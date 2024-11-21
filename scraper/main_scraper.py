from utils import get_hr_page


def main():
    hr_base_url = "https://clerk.house.gov/Votes"
    hr_page = get_hr_page(hr_base_url)
    print(hr_page)


if __name__ == "__main__":
    main()
