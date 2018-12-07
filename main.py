"""Main file to data analysis."""
from app.analysis import main_analysis, plot_dbscan_clicks_on_image, find_value_for_eps, eps_against_num_of_clusters
# from time import time
# ts = time()
main_analysis(15)
# print(time() - ts)
# plot_dbscan_clicks_on_image(
#     "SPIGa/SPIGa2014b_000163.JPG",
#     "Raw_images_SPIG/SPIGa2014/SPIGa2014b_000163.JPG"
# )
# plot_bar()
# from app.db.models import create_tables
# create_tables()
# from app.dataimports import import_data
# import_data('click_data')

# data = [
#     {
#         "image_path": "SPIGa/SPIGa2014b_000163.JPG",
#         "file_path": "Raw_images_SPIG/SPIGa2014/SPIGa2014b_000163.JPG",
#         "penguin_number": 47
#     },
#     {
#         "image_path": "SPIGa/SPIGa2014a_000127.JPG",
#         "file_path": "Raw_images_SPIG/SPIGa2014/SPIGa2014a_000127.JPG",
#         "penguin_number": 42
#     },
#     {
#         "image_path": "SPIGa/SPIGa2014a_000157.JPG",
#         "file_path": "Raw_images_SPIG/SPIGa2014/SPIGa2014a_000157.JPG",
#         "penguin_number": 37
#     },
#     {
#         "image_path": "SPIGa/SPIGa2014a_000211.JPG",
#         "file_path": "Raw_images_SPIG/SPIGa2014/SPIGa2014a_000211.JPG",
#         "penguin_number": 37
#     },
#     {
#         "image_path": "SPIGa/SPIGa2014a_000181.JPG",
#         "file_path": "Raw_images_SPIG/SPIGa2014/SPIGa2014a_000181.JPG",
#         "penguin_number": 34
#     },
#     {
#         "image_path": "SPIGa/SPIGa2014a_000242.JPG",
#         "file_path": "Raw_images_SPIG/SPIGa2014/SPIGa2014a_000242.JPG",
#         "penguin_number": 31
#     },
#     {
#         "image_path": "SPIGa/SPIGa2014b_000007.JPG",
#         "file_path": "Raw_images_SPIG/SPIGa2014/SPIGa2014b_000007.JPG",
#         "penguin_number": 43
#     },
#     {
#         "image_path": "SPIGa/SPIGa2014a_000015.JPG",
#         "file_path": "Raw_images_SPIG/SPIGa2014/SPIGa2014a_000015.JPG",
#         "penguin_number": 36
#     },
#     {
#         "image_path": "SPIGa/SPIGa2014a_000025.JPG",
#         "file_path": "Raw_images_SPIG/SPIGa2014/SPIGa2014a_000025.JPG",
#         "penguin_number": 35
#     },
#     {
#         "image_path": "SPIGa/SPIGa2014a_000039.JPG",
#         "file_path": "Raw_images_SPIG/SPIGa2014/SPIGa2014a_000039.JPG",
#         "penguin_number": 33
#     },
#     {
#         "image_path": "SPIGa/SPIGa2014a_000111.JPG",
#         "file_path": "Raw_images_SPIG/SPIGa2014/SPIGa2014a_000111.JPG",
#         "penguin_number": 37
#     },
# ]

# for d in data:
#     print(find_value_for_eps(d['penguin_number'], d['image_path']))

# # eps_against_num_of_clusters("SPIGa/SPIGa2014b_000163.JPG")