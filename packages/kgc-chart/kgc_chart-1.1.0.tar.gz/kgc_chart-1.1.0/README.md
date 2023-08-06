krüger-gauge-circular-chart is an addition to the gauge-circular-chart. the added feature is another data dimension the chart, by adjusting the bar width of each bar seperately.

below there is a code example.

""" 
import kcg_chart as krueger_circular_gauge_chart

data = {"Pigs":(2,50), "Cows":(3,350), "Dogs":(5,125), "Chickens":(0.7, 20)}

k_c_g_chart = krueger_circular_gauge_chart(data)

k_c_g_chart.draw()

k_c_g_chart.add_labels()

k_c_g_chart.save_and_display_image()

print(k_c_g_chart) """

the data passed is hypothetical data of a farm, with the first element the age at which the animals are slaughtered, the second element the amount of animals slaughtered the main difference between a krüger-gauge-circular-chart and a bar chart with variable bar width is the functionality of display. a bar chart displays the whole amount as an area (A = length * width), which makes sense when the two variables are compatible to multiply (e.g. per Capita CO2 emissions and number of people). However, as seen in the hypothetical data above, this chart type is not compatible, as the interesting fact is not the whole amount of years lived by the animals, but the comparison of amount of animals slaughtered and their age.

est. December 2021
Christoph Krüger