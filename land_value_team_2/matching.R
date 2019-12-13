
library(readr)
full_train <- read_csv("Downloads/full_train.csv")
library('Matching')
# select only numeric variables
nums <- unlist(lapply(full_train, is.numeric))  
df <- full_train[,nums]

#treatment vector
df$e_sold[df$e_sold > 0] <- 1

#covariate
df<- df[, names(df) != 'X1']
df<- df[, names(df) != 'p_e']
df<- df[, names(df) != 'pid']
df<- df[, names(df) != 'p_f']
df<- df[, names(df) != 'p_prot_1990_200']
df<- df[, names(df) != 'p_prot_2000_200']
df<- df[, names(df) != 'p_prot']
df<- df[, names(df) != 'p_prot_2010_200'] 
df<- df[, names(df) != 'ls_price_pc'] 
df<- df[, names(df) != 'p_pasture'] 
df<- df[, names(df) != 'p_crops'] 
df<- df[, names(df) != 'hh_inc_med_bg'] 
df<- df[, names(df) != 'hh_inc_med_tract'] 
df<- df[, names(df) != 'hh_inc_avg_bg'] 
df<- df[, names(df) != 'hh_inc_avg_tract'] 

#maching
m <- Match(df$log_price_per_ha, df$e_sold, df[, (names(df) != 'e_sold')& (names(df) != 'log_price_per_ha')], caliper=1.2, BiasAdjust=T)

#result
summary(m)

mb <- MatchBalance(e_sold~ p_water + river_frontage  + f_year          
                    +p_prot_2000_5000+ p_prot_1990_5000 +p_forest_m     
                               +slope           
                    +p_prot_2010_1000+ p_dev_open+       p_dev_medium   
                    +p_shrub+          lake_importance+ p_forest_e     
                     +ha              +e_year          
                    +p_prot_2010_5000+ p_dev_high      +csd_id          
                    +travel +          p_dev_low        +p_wetland_w     
                   +p_prot_2000_1000+ p_grassland      +fips            
                    +  p_wetland_e               
                    +p_prot_1990_1000  
                                 +p_forest_d      
                    +p_barren+         lake_frontage             
                    +p_wet +year            
                   +pop_dens_bg+      pop_dens_tract    
                       , 
                   data=df, match.out=m, nboots=0)


smd <- c()
for (i in 1:length(cov)) {
  smd <- c(smd, mb$AfterMatching[[i]]$sdiff)
}
mean(abs(smd))









