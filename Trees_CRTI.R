setwd('/Users/yizhuangfang/Dropbox/ImageProcessing/CRTI_Tree_species_identification')
list.files('/Users/yizhuangfang/Dropbox/ImageProcessing/CRTI_Tree_species_identification')

library(dplyr)
library(leaflet)
library(RColorBrewer)

df <- read.csv('Trees_CRTI.csv')


df$category <- factor(sample.int(15L, nrow(df$GENUS), TRUE))

factpal <- colorFactor(topo.colors(15), df$category)
#Species count and sort for top 11

#mylabels <- by(countS, countS["COMMONNAME"], head, n=10)
leaflet(df) %>%
  addTiles() %>%
  setView(lng=-87.95, lat =42.08, zoom = 13)%>%
  addCircleMarkers(~Longitude,
                   ~Latitude,
                   color = ~factpal(GENUS),
                   radius = ~DBH_cm/10,
                   fill = T,
                   fillOpacity = 0.2,
                   opacity = 0.6,
                   popup = paste( paste0(df$COMMONNAME),
                                  paste0("DBH (cm): ", df$DBH_cm),
                                  paste0("Tree Heath: ", df$HEALTHWORD),
                                 sep = ", ")) %>%
  addLegend("bottomright",
            colors = c("orange","green", "red", "blue","orange","green", "red", "black",'orange'),
            labels = c("1","2","3","4","5","6","7","8","9"),
                      title = "Trees in Chicago",
                      opacity = 1)

library(plotly)
S_median <- read.csv('S_median.csv')
plot_ly(S_median, x = ~COMMONNAME, y = ~DBH_cm, type = 'scatter', mode = 'markers', size = ~DBH_cm, color = ~COMMONNAME, colors = 'Paired',
             marker = list(opacity = 0.5, sizemode = 'diameter')) %>%
  layout(title = 'Chicago Trees',
         xaxis = list(showgrid = FALSE),
         yaxis = list(showgrid = FALSE),
         showlegend = FALSE)
