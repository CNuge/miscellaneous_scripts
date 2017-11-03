setwd('/Users/Cam/Desktop/Code/r_users_group')

#install.packages('tidyverse')
#this loads up dplyr, ggplot2, tibble, tidyr, readr, purrr and %>%
library(tidyverse)


#using some credit card default data from Kaggle as an example
#https://www.kaggle.com/uciml/default-of-credit-card-clients-dataset/data


cc_data = read.csv('UCI_Credit_Card.csv')
head(cc_data)
names(cc_data)
sapply(cc_data, class)

cc_dat_readr = read_csv('UCI_Credit_Card.csv')
#can use col_types = c(x = col_double())
#to specify the data type for a given column or a set of
#columns on the import statement

head(cc_dat_readr)
names(cc_dat_readr)
sapply(cc_dat_readr, class)


#######
# filter for subsetting data
#######

#these appear equivalent:
#assume the dplyr:: is for masking concerns?

# dplyr::filter(cc_dat_readr, PAY_5 > 0)
x = filter(cc_dat_readr, PAY_5 > 0)
x

#that is a lot cleaner than base r version of code
y = cc_dat_readr[cc_dat_readr$PAY_5 > 0,]

#sanity check, they return the same results
length(x$ID)
length(y$ID)
length(cc_dat_readr$ID)


######
# find the nas in the dataset
######

all_missing_list = colnames(cc_dat_readr)[colSums(is.na(cc_dat_readr)) > 0]
all_missing_list


cc_dat_readr %>% 
  select_if(function(x) any(is.na(x))) %>%
  colnames() -> f_all_missing_list

f_all_missing_list


##########
#Impute the median for columns with missing values
##########
cc_dat_readr
new_way_dat = cc_dat_readr

cc_data

#old_way
for( i in 1:length(f_all_missing_list)){
	print(f_all_missing_list[i])
	
	#get the global median
	median_all = median(cc_data[, f_all_missing_list[i]], na.rm =TRUE)
	
	#inpute the missing values with the column's median
	cc_data[, f_all_missing_list[i]][is.na(cc_data[, f_all_missing_list[i]])] = median_all
}



#new way, find the median of the column and then replace NAs
impute_median <- function(x){
  ind_na <- is.na(x)
  x[ind_na] <- median(x[!ind_na])
  as.numeric(x)
}

new_way_dat %>% 
  mutate_at(f_all_missing_list, impute_median) -> new_way_dat

head(new_way_dat)
length(new_way_dat$ID)
#about the same length but much cleaner


?read_csv





































