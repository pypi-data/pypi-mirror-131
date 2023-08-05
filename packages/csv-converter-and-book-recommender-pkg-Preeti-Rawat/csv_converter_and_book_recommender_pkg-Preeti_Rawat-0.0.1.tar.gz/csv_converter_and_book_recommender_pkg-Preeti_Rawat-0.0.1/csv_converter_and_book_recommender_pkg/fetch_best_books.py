import pandas as pd
import psycopg2 as pg
import pandas as pds
from sqlalchemy import create_engine
from sqlalchemy import create_engine
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

#this class recommends similar behaviour based on the popularity of the book amoung the library users. Popularity is decided based on 
#how many users have issued any particular book. And studies the similarity between types of book opted by the users. 
class BooksRecommender(object):
    #constructor to initialize 
    # join_on: common column to join the datasets
    # book_title_column: book title column name in the dataset
    # user_column: user column name in the dataset
    # value_column: value column name, based on which analysis to be performed.
    def __init__(self, join_on, book_title_column, user_column, value_column):
        self.join_on=join_on
        self.book_column=book_title_column
        self.user_col=user_column
        self.val_col=value_column
        
    # method helps in getting recommended similar books
    #book_name: name of the book, based on which analysis to be performed to get the recommended books.
    # issued_books: dataframe to holds the details of issued books to the users in the library.
    #books: dataframe to hold the details of all the books in the library database.
    #returns the recommended books for book_name value.
    def get_books(self, book_name, issued_books, books):
        try:
            issued_books_with_book_information = issued_books.merge(books, on=self.join_on)
            recommended_books_name=[]
            #create a pivot with column values as user_id and index as book_name and value will be the how many books issued to the user
            #basically books which are read by user are taken similarity.
            user_book_pivot = issued_books_with_book_information.pivot_table(columns=self.user_col, index=self.book_column, values=self.val_col)
            user_book_pivot.fillna(0, inplace=True)
            user_book_sparse = csr_matrix(user_book_pivot)
            #brute algorithen helps in measuring the distance of every point with other point
            model = NearestNeighbors(algorithm='brute')
            model.fit(user_book_sparse)
            indx=user_book_pivot.index.values.tolist().index(book_name)
            distances, suggestions = model.kneighbors(user_book_pivot.iloc[indx,: ].values.reshape(1, -1))
            for i in range(len(suggestions)):
                recommended_books_name.append(user_book_pivot.index[suggestions[i]])
            return recommended_books_name
        except:
            recommended_books_name=[]
            return recommended_books_name
            