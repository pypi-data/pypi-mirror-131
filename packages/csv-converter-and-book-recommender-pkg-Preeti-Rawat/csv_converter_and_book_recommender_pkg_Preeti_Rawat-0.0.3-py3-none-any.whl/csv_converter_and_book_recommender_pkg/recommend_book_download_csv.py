from .download_csv import CSV_Downloader
from .fetch_best_books import BooksRecommender

#DownloadCSVAndRecommendBooks handles two core functionality of library:
#recommend books based on a book name.
#convert model data to csv and download it.
class DownloadCSVAndRecommendBooks(object):
    #constructor to initialize fields for recommendation of book
    def __init__(self, join_on, book_title_column, user_column, value_column):
        self.joinon=join_on
        self.book_col_name=book_title_column
        self.user_col_name=user_column
        self.value_col=value_column
        
    def recommended_books(self,bookName, issued_book_df, book_df):
        
        book_recc=BooksRecommender(self.joinon, self.book_col_name, self.user_col_name,self.value_col)
        response=book_recc.get_books(bookName, issued_book_df, book_df)
        return response
        
    @classmethod
    def download_csv(model_data):
            csv_downloader=CSV_Downloader(model_data)
            downloaded_csv=csv_downloader.download_csv_file()
            return downloaded_csv
            
            