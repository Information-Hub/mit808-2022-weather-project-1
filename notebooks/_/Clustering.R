library(ggplot2)
library(flexmix)
library(lattice)
library(dplyr) 
library(gridExtra)
library(rgl)
library(plot3D)
library(mvtnorm)

set.seed(29)

#Load work book
setwd("C:/Users/gf2704928/Documents/_MIT (Desktop)/__DataFor808/Modeling")
data<-read.csv("leptoDataCombined.csv",sep=",")
data <- as.data.frame(data)
head(data)
data.zscore <- cbind(data[,1:5],scale(data[,6:9]),data[,10])
names(data.zscore) <- c('X', 'Id','Timeframe','Year', 'Lepto_Y_N','rainfall','temperature_max ','temperature_min','temperature_diff','Infes')

data.zscore <- data.zscore[data.zscore$Timeframe >8 & data.zscore$Timeframe <14, ]  

head(data.zscore)
data.zscore

model <- flexmix(data.zscore$Infes ~ data.zscore$temperature_diff  + data.zscore$rainfall, k = 5)
summary(model)
data.clusters <- cbind(data.zscore,clusters(model))
data.clusters
write.csv(data.clusters,file='data.clusters.csv', row.names = FALSE)

# Modelplot <- ggplot(data.clusters)
# Modelplot <- Modelplot + geom_point(aes(x=Timeframe,y=Value,col = c("1", "2", "3","4","5")[clusters(model)]),alpha = 0.6)
# Modelplot
# Modelplot <- Modelplot + scale_color_manual("", values=c("red", "blue", "limegreen","orange","black"), labels=c("red", "blue", "limegreen","orange","black"))
# # Modelplot <- Modelplot + scale_x_continuous(breaks = xrange,labels = xrange, limits = c(-0.5,3))
# # Modelplot <- Modelplot + scale_y_continuous(breaks = yrange2,labels = yrange2, limits = ylimits2)
# Modelplot <- Modelplot + geom_abline(intercept = parameters(model)[1,1], slope = parameters(model)[2,1], col = "red",lwd = 1)
# Modelplot <- Modelplot + geom_abline(intercept = parameters(model)[1,2], slope = parameters(model)[2,2], col = "blue",lwd = 1)
# Modelplot <- Modelplot + geom_abline(intercept = parameters(model)[1,3], slope = parameters(model)[2,3], col = "limegreen",lwd = 1)
# Modelplot <- Modelplot + geom_abline(intercept = parameters(model)[1,4], slope = parameters(model)[2,4], col = "orange",lwd = 1)
# Modelplot <- Modelplot + geom_abline(intercept = parameters(model)[1,5], slope = parameters(model)[2,5], col = "black",lwd = 1)
# Modelplot <- Modelplot + theme(legend.position = "none")
# Modelplot
data.clusters


names(data.clusters) <- c('X', 'Id','Timeframe','Year', 'Lepto_Y_N','rainfall','temperature_max ','temperature_min','temperature_diff','Group')
mycolors <- c("red", "blue", "limegreen","black","orange")
data.clusters$color <- mycolors[ as.numeric(data.clusters$Group) ]

# Plot
plot3d( 
  x=data.clusters$temperature_diff, y=data.clusters$rainfall, z=data.clusters$Timeframe, 
  col = data.clusters$color, 
  type = 's', 
  radius = 0.1)

,
xlab="temperature_diff", ylab="rainfall", zlab="Timeframe"
