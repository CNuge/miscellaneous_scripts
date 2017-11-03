setwd('/Users/Cam/Desktop/Alana') #change this

#this is where you loaded the data in
t1 = read.table('test1.txt', sep='\t',header=T)
t2 = read.table('test.txt', sep='\t',header=T)

# check that these match your data type
t1
t2

#this below would be the list of files you made
flight_sims = list(t1,t2)

#we make an empty dataframe we will add to
new_df = data.frame(matrix(ncol = 2, nrow = 0))
columns = c('id','data_col')
colnames(new_df) = columns

new_df #check the headers are right


#you could add an additional column in below if you wish to retain more data
for(bfly in flight_sims){
	id = names(bfly)[1]	 #this relies on the first column being the id name
	dat = data.frame(id=rep(id, length(bfly[,id])), data_col =list(bfly[id]))
	colnames(dat) = columns
	new_df = rbind(new_df, dat)
}

#this is your dataframe with the id's of the butterflies in col 1 
#and the data is now in column 1
new_df #can save this to a .csv

