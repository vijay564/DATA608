#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(dplyr)
library(tidyr)
library(ggplot2)
library(tibble)
rsconnect::setAccountInfo(name='vijay-564',
                          token='20735163BD1BDFEF6D2CE063989635CE',
                          secret='46r6am8928lFkYap7RN7doZj7dm6XwtLWVcf0mjW')

cdc_url <- "https://raw.githubusercontent.com/charleyferrari/CUNY_DATA608/master/lecture3/data/cleaned-cdc-mortality-1999-2010-2.csv"
cdc <- read.csv(cdc_url, header= TRUE, stringsAsFactors=TRUE)
#change population back into a numeric
cdc$Population <- as.numeric(cdc$Population)
# summarizing data
head(cdc)
summary(cdc)



library(sqldf)
library(ggplot2)
library(rsconnect)
cdc1<-sqldf("
select 
icd_chapter, State, crude_rate 
from 
(
select 
            `ICD.Chapter` as icd_chapter, State, Deaths,Population,power(10,5)*(Deaths/Population) as crude_rate
            from cdc
            where year in ('2010')
            group by `ICD.Chapter`, State
) group by 1,2, 3")
            ggplot(cdc1, aes(fill=icd_chapter, y=crude_rate, x=State)) +
                labs(x="State", y="Crude Death Rate per 100,000 Persons") +  
                geom_bar(stat="identity") +
                coord_flip()
            
            ui <- fluidPage(
                sidebarPanel(
                    selectInput(inputId = "CauseDeath", label = "Cause of Death:",
                                choices = levels(as.factor(cdc1$icd_chapter))
                    ),
                    helpText("States by crude mortality for each cause of death."),
                    width = "auto"
                ),
                plotOutput("plot1")
            )
            server<- function(input, output) {
                
                output$plot1 <-renderPlot({
                    
                    SelectedCause <- input$CauseDeath
                    
                    ggplot(data=cdc1[cdc1$icd_chapter == SelectedCause,]
                           , aes(x = State, y = crude_rate)) +
                        labs(x="State", y="Crude Death Rate", 
                             title = "Crude death rate per 100,000 persons",
                             subtitle = paste("Caused by", SelectedCause)) +  
                        geom_bar(stat="identity", fill="steelblue") + 
                        geom_hline(aes(yintercept = mean(crude_rate, na.rm = TRUE), linetype = "National Average"), col="red", lwd=1) +
                        scale_linetype(name = NULL) +
                        theme_bw()
                    
                })
            }
shinyApp(ui = ui, server = server)
#deployApp()
            
            
# Run the application 
shinyApp(ui = ui, server = server)
