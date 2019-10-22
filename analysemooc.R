# Install the package in R
#install.packages("RPostgreSQL")

library(RPostgreSQL)
library(DBI)
library(readr)



## Loading required package: DBI

# library(getPass)
pgdrv <- dbDriver(drvName = "PostgreSQL")

BDD <-DBI::dbConnect(pgdrv,
                    dbname="BDD_Tarik",
                    host="127.0.0.1", port=5433,
                    user = 'team',
                    password = 'DataLab@2019')
                  


Table1 <- RPostgreSQL::dbReadTable(BDD, "MoocWeb")
DBI::dbDisconnect(BDD)


library(magrittr)
  

library(ggplot2)

ggplot(Table1) +
  aes(x = date) +
  geom_histogram(bins = 30L, fill = "#0c4c8a") +
  theme_minimal()

#librairie facet message par jour par user



library(ggplot2)

ggplot(Table1) +
 aes(x = date) +
 geom_histogram(bins = 30L, fill = "#0c4c8a") +
 theme_minimal() +
 facet_wrap(vars(username))

library(dplyr)
library(wordcloud2)
wordcloud2(Table1$message, size=1.6)

library(ggplot2)

ggplot(Table1) +
 aes(x = username, fill = username, size = username, angle = 90) +
 geom_bar() +
 scale_fill_hue() +
 theme_classic()

  ggplot(Table1) +
    aes(x = level, group = message) +
    geom_histogram(bins = 30L, fill = "#0c4c8a") +
    theme_minimal()
  
  
ggplot(Table1) +
  aes(x = date, group = message) +
  geom_bar(bins = 30L, fill = "#0c4c8a") +
  theme_minimal()


ggplot(Table1) +
  aes(x = date, group = message) +
  geom_bar(fill = "#fb6a4a") +
  theme_classic()


ggplot(Table1) +
  aes(x = username, fill = username, colour = username, size = level, group = message) +
  geom_bar() +
  scale_fill_hue() +
  scale_color_hue() +
  theme_classic()

library(gmodels)
d<-CrossTable(Table1$username, Table1$message) 
