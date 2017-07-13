library('randomForest')
library('tidyverse')



############
# iterative randomforest drop
############
#this function will perform a random forest regression on the data, drop the lowest
#predictor, and then repeat the process until the best predictor is identified
#it will return a dataframe with the pseudo-rsquared
#note the ntree parameter in the loop, tune this to the desired size

iterative_rf_drop = function(input_dataframe, y_column, predictor_columns){
	outdf = data.frame(size=numeric(),oob_mse=numeric(),lowest_predictor=character())
	cols_to_use = c(y_column, predictor_columns)
	rf_input=select(input_dataframe,one_of(cols_to_use))	
	while(length(names(rf_input)) > 1){
		#train the model
		rf_result = randomForest(rf_input[,y_column]~., data = rf_input, ntree = 10000, importance = TRUE)
		#obtain the out-of-bag prediction using predict function
		oob_prediction = predict(rf_result)
		#calculate test_mse based on the 
		test_mse = mean((oob_prediction - rf_input[,y_column])^2)
				
		#find the worst predictor, add its name to the dataframe and drop column
		importance_dat = rf_result$importance
		sorted_predictors = sort(importance_dat[,1], decreasing=TRUE)
		worst_pred = names(sorted_predictors[length(sorted_predictors)])
		out_line = data.frame(size=length(sorted_predictors), oob_mse=test_mse, lowest_predictor=worst_pred)
		outdf = rbind(outdf,out_line)
		rf_input = rf_input[, !colnames(rf_input) %in% worst_pred]
	}
	return(outdf)
	}


czri_dat = read.csv('CZRI_rf_input.csv')
head(czri_dat)
names(czri_dat)
length(names(czri_dat))
#data stored in 
#repeated list of nodes after that
#1396 predictor values.
y_values = c("fish","Weight1","Length1","Weight2","Length2")
x_values = names(czri_dat)[6:length(names(czri_dat))]

for(name in x_values){
	czri_dat[,name]= as.factor(czri_dat[,name])
}

summary(czri_dat)


############
# Weight at time 1
############
set.seed(10)
rf_weight1 = randomForest(Weight1~.-Length1-Weight2-Length2-fish, data = czri_dat, ntree = 10000, importance = TRUE)
importance(rf_weight1)
varImpPlot(rf_weight1)
mean(rf_weight1$rsq)
#output the variable importance to a csv
rf_weight1$mse
names(rf_weight1)
#problem... the % variance explained is far too low.
#          Mean of squared residuals: 7331.356
#                    % Var explained: 0.52
#need to perform feature selection to remove noise from dataset
summary(rf_weight1)
predict(rf_weight1)

importance_order = order(-rf_weight1$importance)
importance_dat = rf_weight1$importance
variance_explained = mean(rf_weight1$rsq) * 100
#col 1 is %incMSE col2 is IncNodePurity

#sort the best predictors
sorted_predictors = sort(importance_dat[,1], decreasing=TRUE)
best_predictors = sorted_predictors[1:100]
predictor_columns = names(best_predictors)
y_column = c('Weight1')
#run the iterative dropfunction, performing a rf regression for each feature set
model_selection = iterative_rf_drop(czri_dat, y_column, predictor_columns)
model_selection

plot( model_selection$size,model_selection$oob_mse)


#lowest MSE seen with these 20 loci... note that AC08m and AC13f are present in high quantities
best_predictors=c("AC06m.2_C3","AC33f_C0","AC06m.2_C11","AC06m.2_C12","AC08m_C11","AC13f.1_C18","AC13f.1_C15","AC08m_C6","AC06m.2_C17","AC13f.1_C21","AC13f.1_C17","AC08m_C4","AC08m_C8","AC13f.1_C9","AC13f.1_C16","AC13f.1_C10","AC13f.1_C20","AC13f.1_C14","AC08m_C12","AC08m_C13")

#subset the dataframe, with just the columns in the best predictor list
refined_columns = c(y_column, best_predictors)
rf_refined=select(czri_dat,one_of(refined_columns))
#train model
rf_weight1_refined = randomForest(Weight1~., data = rf_refined, ntree = 10000, importance = TRUE)
rf_weight1_refined 
names(rf_weight1_refined)
rf_weight1_refined$call
#reduced model explains 34% of the variation in weight seen! thats a huge improvement!
#9 from AC13f, 6 from AC08 and 3 from AC06m




