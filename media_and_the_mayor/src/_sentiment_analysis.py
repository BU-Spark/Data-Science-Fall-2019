##############################################################################################
# THIS CODE IS COPIED FROM THE GLUON NLP SENTIMENT ANALYSIS DOCUMENTATION
import warnings
warnings.filterwarnings('ignore')

import random
import time
import multiprocessing as mp
import numpy as np
import pandas as pd

import mxnet as mx
from mxnet import nd, gluon, autograd

import gluonnlp as nlp
# nlp.utils.check_version('0.7.0')


MODELS = './Models/'

random.seed(123)
np.random.seed(123)
mx.random.seed(123)



class MeanPoolingLayer(gluon.HybridBlock):
	"""A block for mean pooling of encoder features"""
	def __init__(self, prefix=None, params=None):
		super(MeanPoolingLayer, self).__init__(prefix=prefix, params=params)

	def hybrid_forward(self, F, data, valid_length): # pylint: disable=arguments-differ
		"""Forward logic"""
		# Data will have shape (T, N, C)
		masked_encoded = F.SequenceMask(data,
										sequence_length=valid_length,
										use_sequence_length=True)
		agg_state = F.broadcast_div(F.sum(masked_encoded, axis=0),
									F.expand_dims(valid_length, axis=1))
		return agg_state


class SentimentNet(gluon.HybridBlock):
	"""Network for sentiment analysis."""
	def __init__(self, dropout, prefix=None, params=None):
		super(SentimentNet, self).__init__(prefix=prefix, params=params)
		with self.name_scope():
			self.embedding = None # will set with lm embedding later
			self.encoder = None # will set with lm encoder later
			self.agg_layer = MeanPoolingLayer()
			self.output = gluon.nn.HybridSequential()
			with self.output.name_scope():
				self.output.add(gluon.nn.Dropout(dropout))
				self.output.add(gluon.nn.Dense(1, flatten=False))

	def hybrid_forward(self, F, data, valid_length): # pylint: disable=arguments-differ
		encoded = self.encoder(self.embedding(data))  # Shape(T, N, C)
		agg_state = self.agg_layer(encoded, valid_length)
		out = self.output(agg_state)
		return out



dropout = 0
language_model_name = 'standard_lstm_lm_200'
pretrained = True
learning_rate, batch_size = 0.005, 32
bucket_num, bucket_ratio = 10, 0.2
epochs = 1
grad_clip = None
log_interval = 100

context = mx.cpu()

lm_model, vocab = nlp.model.get_model(
	name = language_model_name, 
	dataset_name = 'wikitext-2', 
	pretrained = pretrained, 
	ctx = context, 
	dropout = dropout
)

net = SentimentNet(dropout=dropout)
net.embedding = lm_model.embedding
net.encoder = lm_model.encoder
net.hybridize()
net.output.initialize(mx.init.Xavier(), ctx=context)
print(net)


# The tokenizer takes as input a string and outputs a list of tokens.
tokenizer = nlp.data.SpacyTokenizer('en')

# `length_clip` takes as input a list and outputs a list with maximum length 500.
length_clip = nlp.data.ClipSequence(500)


# Helper function to preprocess a single data point
def preprocess(x):
	data, label = x
	label = int(label > 5)
	# A token index or a list of token indices is
	# returned according to the vocabulary.
	data = vocab[length_clip(tokenizer(data))]
	return data, label


# Helper function for getting the length
def get_length(x):
	return float(len(x[0]))



# Loading the dataset
train_dataset, test_dataset = [nlp.data.IMDB(root='data/imdb', segment=segment)
							   for segment in ('train', 'test')]
print('Tokenize using spaCy...')



def preprocess_dataset(dataset):
	start = time.time()
	with mp.Pool() as pool:
		# Each sample is processed in an asynchronous manner.
		dataset = gluon.data.SimpleDataset(pool.map(preprocess, dataset))
		lengths = gluon.data.SimpleDataset(pool.map(get_length, dataset))
	end = time.time()
	print('Done! Tokenizing Time={:.2f}s, #Sentences={}'.format(end - start, len(dataset)))
	return dataset, lengths



# Doing the actual pre-processing of the dataset
train_dataset, train_data_lengths = preprocess_dataset(train_dataset)
test_dataset, test_data_lengths = preprocess_dataset(test_dataset)



# Construct the DataLoader
def get_dataloader():

	# Pad data, stack label and lengths
	batchify_fn = nlp.data.batchify.Tuple(
		nlp.data.batchify.Pad(axis=0, pad_val=0, ret_length=True),
		nlp.data.batchify.Stack(dtype='float32'))
	batch_sampler = nlp.data.sampler.FixedBucketSampler(
		train_data_lengths,
		batch_size=batch_size,
		num_buckets=bucket_num,
		ratio=bucket_ratio,
		shuffle=True)
	print(batch_sampler.stats())

	# Construct a DataLoader object for both the training and test data
	train_dataloader = gluon.data.DataLoader(
		dataset=train_dataset,
		batch_sampler=batch_sampler,
		batchify_fn=batchify_fn)
	test_dataloader = gluon.data.DataLoader(
		dataset=test_dataset,
		batch_size=batch_size,
		shuffle=False,
		batchify_fn=batchify_fn)
	return train_dataloader, test_dataloader

# Use the pre-defined function to make the retrieval of the DataLoader objects simple
train_dataloader, test_dataloader = get_dataloader()


def evaluate(net, dataloader, context):
	loss = gluon.loss.SigmoidBCELoss()
	total_L = 0.0
	total_sample_num = 0
	total_correct_num = 0
	start_log_interval_time = time.time()

	print('Begin Testing...')
	for i, ((data, valid_length), label) in enumerate(dataloader):
		data = mx.nd.transpose(data.as_in_context(context))
		valid_length = valid_length.as_in_context(context).astype(np.float32)
		label = label.as_in_context(context)
		output = net(data, valid_length)

		L = loss(output, label)
		pred = (output > 0.5).reshape(-1)
		total_L += L.sum().asscalar()
		total_sample_num += label.shape[0]
		total_correct_num += (pred == label).sum().asscalar()

		if (i + 1) % log_interval == 0:
			print('[Batch {}/{}] elapsed {:.2f} s'.format(
				i + 1, len(dataloader),
				time.time() - start_log_interval_time))
			start_log_interval_time = time.time()

	avg_L = total_L / float(total_sample_num)
	acc = total_correct_num / float(total_sample_num)

	return avg_L, acc


def train(net, context, epochs):
	trainer = gluon.Trainer(net.collect_params(), 'ftml',
							{'learning_rate': learning_rate})
	loss = gluon.loss.SigmoidBCELoss()

	parameters = net.collect_params().values()

	# Training/Testing
	for epoch in range(epochs):
		# Epoch training stats
		start_epoch_time = time.time()
		epoch_L = 0.0
		epoch_sent_num = 0
		epoch_wc = 0
		# Log interval training stats
		start_log_interval_time = time.time()
		log_interval_wc = 0
		log_interval_sent_num = 0
		log_interval_L = 0.0

		for i, ((data, length), label) in enumerate(train_dataloader):
			L = 0
			wc = length.sum().asscalar()
			log_interval_wc += wc
			epoch_wc += wc
			log_interval_sent_num += data.shape[1]
			epoch_sent_num += data.shape[1]
			with autograd.record():
				output = net(data.as_in_context(context).T,
							 length.as_in_context(context)
								   .astype(np.float32))
				L = L + loss(output, label.as_in_context(context)).mean()
			L.backward()
			# Clip gradient
			if grad_clip:
				gluon.utils.clip_global_norm(
					[p.grad(context) for p in parameters],
					grad_clip)
			# Update parameter
			trainer.step(1)
			log_interval_L += L.asscalar()
			epoch_L += L.asscalar()
			if (i + 1) % log_interval == 0:
				print(
					'[Epoch {} Batch {}/{}] elapsed {:.2f} s, '
					'avg loss {:.6f}, throughput {:.2f}K wps'.format(
						epoch, i + 1, len(train_dataloader),
						time.time() - start_log_interval_time,
						log_interval_L / log_interval_sent_num, log_interval_wc
						/ 1000 / (time.time() - start_log_interval_time)))
				# Clear log interval training stats
				start_log_interval_time = time.time()
				log_interval_wc = 0
				log_interval_sent_num = 0
				log_interval_L = 0
		end_epoch_time = time.time()
		test_avg_L, test_acc = evaluate(net, test_dataloader, context)
		print('[Epoch {}] train avg loss {:.6f}, test acc {:.2f}, '
			  'test avg loss {:.6f}, throughput {:.2f}K wps'.format(
				  epoch, epoch_L / epoch_sent_num, test_acc, test_avg_L,
				  epoch_wc / 1000 / (end_epoch_time - start_epoch_time)))


		trainer.save_states(MODELS + 'sentiment_analysis.states')



train(net, context, epochs)
##############################################################################################
import os



# define the required paths
DATASETS = './Datasets/'
FILTERED_DATASETS = DATASETS + 'Filtered/'
SENTIMENT_DATASETS = DATASETS + 'Sentiment/'



datasets = os.listdir(FILTERED_DATASETS)
for file in datasets:
	# make predictions on the sentiment of each article
	if file.endswith('.csv'):
		predictions = []
		df = pd.read_csv(FILTERED_DATASETS + file)

		for i, article in df.iterrows():
			article_text = ' '.join(article['text'].strip('[').strip(']').split()).split()
			sentiment_prediction = net(
				mx.nd.reshape(
					mx.nd.array(vocab[article_text], ctx=context), 
					shape=(-1, 1)
					), 
				mx.nd.array([4], ctx=context)
				).sigmoid()

			predictions.append(sentiment_prediction[0])


		df['raw_sentiment'] = predictions
		if not os.path.exists(SENTIMENT_DATASETS):
			os.mkdir(SENTIMENT_DATASETS)

		df.to_csv(SENTIMENT_DATASETS + file, index=False)







