from bs4 import BeautifulSoup
import requests
import pandas as pd

#find number of pages
root_url = 'https://www.glassdoor.com/Explore/top-companies-belgrade_IL.14,22_IM1655.htm'
source = requests.get(root_url, headers={'User-Agent':'Mozzila/5.0'}).text
soup = BeautifulSoup(source, 'lxml')
last_page = soup.find_all('button', class_='pagination__PaginationStyles__paginationButton d-flex align-items-center justify-content-center')[-1].text
page_list = list(range(1, int(last_page)+1))

#data fields
company_name = []
location = []
size = []
industry = []
desc = []
link = []
reviews_count = []
salaries_count = []
jobs_count = []

for page in page_list:

    url = f'https://www.glassdoor.com/Explore/browse-companies.htm?overall_rating_low=3.5&page={page}&isHiringSurge=0&locId=1655&locType=M&locName=Belgrade,%20Serbia%20Area'
    source = requests.get(url, headers={'User-Agent': 'Mozzila/5.0'}).text
    soup = BeautifulSoup(source, 'lxml')
    companies = soup.find_all('section', class_='employerCard__EmployerCardStyles__employerCard common__commonStyles__module p-std mt-0 mb-std mx-std mx-sm-0')

    for company_post in companies:

        company_name.append(company_post.find('h2').text.strip())
        location.append(company_post.find('span', {'data-test':'employer-location'}).text.strip())
        size.append(company_post.find('span', {'data-test':'employer-size'}).text.strip())
        industry.append(company_post.find('span', {'data-test':'employer-industry'}).text.strip())
        desc.append(company_post.find('p', class_='employerCard__EmployerCardStyles__clamp common__commonStyles__subtleText').text.strip())
        link.append(company_post.find('div', class_='col-12 my-0 mt-sm mt-sm-std order-5').find('a', href=True)['href'])
        reviews_count.append(company_post.find('div', {'data-test':'cell-Reviews-count'}).text.strip())
        salaries_count.append(company_post.find('div', {'data-test':'cell-Salaries-count'}).text.strip())
        jobs_count.append(company_post.find('div', {'data-test':'cell-Jobs-count'}).text.strip())

data = {
    'company_name': company_name,
    'location': location,
    'size': size,
    'industry': industry,
    'desc': desc,
    'link': link,
    'reviews_count': reviews_count,
    'salaries_count': salaries_count,
    'jobs_count': jobs_count
}

df = pd.DataFrame(data)
df.to_csv('data.csv')
print(df.head())