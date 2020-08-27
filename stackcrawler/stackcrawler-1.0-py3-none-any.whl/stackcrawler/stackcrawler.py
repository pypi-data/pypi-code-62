from bs4 import BeautifulSoup
import requests
from array import array


"""
This is an example of Web Scrapping mean extract the data from

the particular website e.g 'https://stackoverflow.com/questions' and

Display result as an output on the terminal.
"""

def stackoverflow(page_number: int):
  """ It fetches Question from the stackoverflow/question Webportal.
    
  Parameters:

  page_number (int): Page number b\w 1 to 20 Only. 
  example : 10

  Return:
  Int : Number of page/pages need to be fetch.
  """
  page_len = 0
  total_question = 0
  print(f"\n\033[33mYou have Select \033[31m{page_number} \033[33mnumber for Web Pagination\033[37m")
  # Pagination of Web Page Number.
  try:
      page_number = int(page_number)
      if page_number >= 1 and page_number <= 20:

          while page_len < page_number:

              page_len += 1
              print(
                  f'\n\033[33m-----Welcome to Page No {page_len}-----\033[37m\n'.center(250))
              next_page = f"https://stackoverflow.com/questions?tab=newest&page={page_len}"
              response = requests.get(next_page)
              soup = BeautifulSoup(response.text, "html.parser")
              questions = soup.select(".question-summary")

              for num, question in enumerate(questions, 1):
                  print(
                      f"\033[37mQuestion {num}) \033[32m{question.select_one('.question-hyperlink').getText().strip('?')}?")
                  print(
                      f"\033[37mAnswer {num}) \033[31m{question.select_one('.vote-count-post').getText()}\n")
              total_question += num

              print(
                  f'\n\033[33m-----End of Page No {page_number}------\033[37m'.center(250))

          print(
              f"\n\033[33mThere are Total \033[31m{total_question}\033[33m Question with answers.\n\033[33m")

      else:
          print("\033[32mEnter Page Number between 1 to 20 only\033[37m")

  except Exception as e:
      print(e)

  print("""
\033[34m
This Project is created by Bhatia's software solutions corporation.
Author: \033[37mAsh Bhatia\033[34m
Source: \033[37mhttps://stackoverflow.com/questions\033[34m
Version: \033[37m1.1.0\033[34m
Email: \033[37mashbhatia2@gmail.com\033[34m
Copyright: \033[37mBhatia's software solutions corporation

""")

stackoverflow(1)