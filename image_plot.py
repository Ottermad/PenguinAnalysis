"""Plot Clicks on Image."""
from app.analysis.dbscan import plot_dbscan_clicks_on_image
from app.analysis.meanshift import plot_meanshift_clicks_on_image
plot_dbscan_clicks_on_image(
    'SPIGa/SPIGa2014a_000005.JPG',
    'Raw_images_SPIG/SPIGa2014/SPIGa2014a_000005.JPG',
    19
)

plot_meanshift_clicks_on_image(
    'SPIGa/SPIGa2014a_000005.JPG',
    'Raw_images_SPIG/SPIGa2014/SPIGa2014a_000005.JPG',
    28
)
