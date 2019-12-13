# CS506-Project

Analysis of Federal Grants for Minority Business Enterprises for the Office of Congressman Joe Kennedy III
Yong Zhou, Yue Yu and Ghislaine de Bree

Advisor: Professor Lance Galletti
Client (on behalf of the Congressman’s Office): John Merfeld


Motivation

The project will analyze several different datasets to examine how federal grants are awarded to business enterprises in Massachusetts, and in particular to Massachusetts Minority Business Enterprises (MBEs). The office of Joe Kennedy III, the Congressman for Massachusetts’ Fourth District, suspects a potential discrepancy in the number of grants awarded to Black and Latinx owned businesses and, therefore, has requested on this project that investigates the proportion of federal grants awarded to MBEs. The results of the project will provide the number and percentage of Massachusetts (MA) businesses receiving federal grant money that are Black/LatinX owned and any unusual/unexpected or additional findings.
The grants awarded that we will look into for this study can come from seven different government agencies:
●    Massachusetts Department of Transportation (DOT)
●    Small Business Innovation Research (SBIR)
●    US Department of Housing and Urban Development (HUD)
●    The US Department of Health and Human Services (HHS)
●    Federal Emergency Management Agency (FEMA)
●    Environmental Protection Agency (EPA)
●    National Science Foundation (NSF)

In looking at the make-up of recipients of federal grants, we expect to find a disproportionately large amount of grants given to non-MBE businesses. The ultimate aim of the project, given we find truth in the assumption of unfair federal grant allocation, is to give the Congressman grounds for advocating for a more inclusively-minded grant awarding process by federal agencies.


Exploratory Goals

In order to reach the goal of finding the proportion of Black and Latinx owned MBEs in Massachusetts receiving grants from federal funding agencies, our group will go through four main phases. The majority of our data exploration will occur in the last two phases as here we will be able to look into strategic questions that go beyond the central focus of the project.



Data Scraping

Our team will scrape data from specific group of federal agencies, as listed above, in order to find federal grants awarded to businesses owned in Massachusetts. The USA Spending API will be our main point of interaction with the data, as we will use it to focus on award data from the specified government agencies. Fortunately, Government datasets tend to be very well maintained, but our problem is in dataset size. Filtering data before accessing locally will be vital because the data is maintained on a federal level, and the project only requires us to look into data concerning Massachusetts.


Data Cleaning and Consolidation

In this stage the focus is not yet on MBEs, but rather on cleaning and formulating a general dataset which will later be used to create a picture of how MBEs fit into the process of awarding grants. Our main focus here is to create one dataset with a range of potentially impactful attributes. Initial thought has led us to aim to refine our data while including the following attributes:
●    A Unique Identifier (DUNS Number)
●    Company Name
●    Type of the Recipient (for example non-profit, small business, corporation, institute for higher learning)
●    Industry of Recipient
●    Grant Name
●    Federal Agency (i.e. the Source of the Grant)
●    Amount Awarded
●    Date of Grant

Further inspection of potential influencers will be refined and altered based on their relevance to how grants are awarded to MBEs.


Incorporation of Minority Owned Businesses Data Sources

Once the federal grants data set has been solidified, we will begin working with our MBE data sources, namely the Small Business Association and the US Black Chamber of Commerce. By using data from both of these sources, instances of grants given to MBEs in the federal awards dataset can be highlighted. The extent to which we will incorporate attributes from the smaller MBE datasets into our larger awards dataset will depend on how the data is formed, but the name of the executive and their ethnicity will be included. Given the combination of the datasets in this phase, we will begin to look into the specifics of strategic questions surrounding the main focus of our project. The client has asked that a few specific topics are considered, including the

size of enterprises that are awarded grants and how federal grants for MBE are being used in Boston. Suffolk County is both the largest and most diverse county in the state, so it would make intuitive sense that the majority of federal grants awarded, and specifically those awarded to minorities, come into Boston.


Final Deliverable

Based on the technology mentioned above, we will come up with specific suggestions based on the results of this analysis. By the prospective results we will find the proportion of grants awarded to Black and Latinx owned businesses to the total number of MA businesses receiving federal grant money. This will allow us to determine the correctness of the assumptions from the Congressman's office. Furthermore, by our data, we will dig out more valuable results and give suggest to Congressman's office to make further decisions on the businesses awarded for the future. Specifically, we hope to look into the types of sectors in which MBEs are being awarded federal grants and what these contracts look like, in terms of length or size. The size of the businesses receiving grants is also of interest to us, as we assume that this may have an impact on federal agencies’ choices in allocation of grants. We are also will look into how federal grants are given to the same businesses over extended periods of time, and how this may impact MBEs.


Non-goals
We believe that inference based on our results is beyond the scope of our capabilities and therefore we will not do further inference on the causes or consequences of our result nor provide solutions for any potential realistic problems inferenced from our final result. As the project is limited to the semester, we will not collect or generate any new data for the funding information for minority owned businesses.


Hypothesis
The client has requested a few specific questions be answered in our research, and we will be able to include conclusions to these in our final product. We will create an image of what federal grants given to MBEs look like, and what type of MBEs receive them. We will report the number of percentages of federal grants awarded in Massachusetts that are given to Black and Latinx owned business enterprises. In doing so we uncover the composition of these grants, showing which grants are given to Black and Latinx owned businesses. Our hypothesis here is that the Congressman’s office is correct in suspecting that the number of Black and Latinx owned business enterprises receiving federal grants is far lower than proportional.
In our team’s definition, a fair proportion of federal grants given to MBEs is equal to the percentage of MBEs (and specifically Black and Latinx owned MBEs) in a specific sector or the

percentage within a group of enterprises that have eligibility for federal grants from a specific funding agency. However, it can be argued that the proportion of MBEs in a specific sector may be lower than the population percentage would predict because of the issue of federal agencies overlooking MBEs, and therefore lowering their ability to function. We would therefore hope that there will be an increase of federal funding to MBEs beyond proportional, if our assumptions are correct, so that there may be a higher overall proportion of MBEs working in specific sectors.


Final Product

The main focus of our project is investigating number and percentage of Black and Latinx owned MBEs receiving federal grant money, from a variety of government agencies. In order to present this information intelligibly, our final product will include an outline of how our team worked through the steps described above and further explanation of specific methods used.
There will be inevitable obstacles and unexpected findings that come out of our investigation, and these issues and the potential impacts that they have on our final outcomes will be presented. The final product will also include a detailed explanation of the data sources and specific attributes used in our exploration.
There is likely to be a high variation in our hypothesis about issues surrounding our central focus, so we do expect that our findings will not strictly align with our central hypothesis, as described above. The results of the analysis will not only define the percentages of the total grants awarded to MA businesses that are awarded to MBEs, but will also create a larger image of how differing factors impact a businesses’ likelihood to receiving federal or state level funding.
