import requests as requests
from bs4 import BeautifulSoup


def extration_data():
    """

    date:09 Desember 2021, 0
    Time:2:00:53 WIB
    magnitudo:5.1
    depth:249 km
    location: LS=7.85 BT=-123.44
    epicenter: 69 km Nortwest LEMBATA-NTT
    be perceived:no tsunami potential
    :return:
    """
    try:
        content = requests.get('https://bmkg.go.id')
    except  Exception:
        return None
    if content.status_code == 200:
        soup = BeautifulSoup(content.text, 'html.parser')

        conclusion = soup.find('span', {'class': 'waktu'})
        conclusion = conclusion.text.split(', ')
        date = conclusion[0]
        time = conclusion[1]

        conclusion = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
        conclusion = conclusion.findChildren('li')
        i = 0
        magnitudo = None
        depth = None
        ls = None
        bt = None
        location = None
        be_perceived = None



        for res in conclusion:
                print(i, res)
                if i == 1:
                    magnitudo = res.text
                elif i == 2:
                    depth = res.text
                elif i == 3:
                    coordinate = res.text.split(' - ')
                    ls = coordinate[0]
                    bt = coordinate[1]
                elif i == 4:
                    location = res.text
                elif i == 5:
                    be_perceived = res.text
                i = i+1



        conclusion = dict()
        conclusion['date'] = date
        conclusion['time'] = time
        conclusion['magnitudo'] = magnitudo
        conclusion['depth'] = depth
        conclusion['location'] = location
        conclusion['coordinate'] = {'ls': ls, 'bt': bt}
        conclusion['be perceived'] = be_perceived
        return conclusion
    else:
        return None

def show_data(result):
    if result is None:
        print("No one can find data last eartquake data")
    print('The last eartquake based on BMKG')
    print(f"Date {result['date']}")
    print(f"Time {result['time']}")
    print(f"Magnitudo {result['magnitudo']}")
    print(f"Depth {result['depth']}")
    print(f"Location {result['location']}")
    print(f"Coordinate:LS={result['coordinate']['ls']}, BT={result['coordinate']['bt']}")
    print(f"Be perceived {result['be perceived']}")


if __name__ == '__main__':
    result = extration_data()
    show_data(result)