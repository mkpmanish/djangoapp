#!/usr/bin/python
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from urllib.parse import urljoin

"""
Problem Statement:-

4. Write a python or go script to: 
    1. Fetch all code scanning alerts for above repo with severity High or above
    2. Obtain ‘Likelihood of exploitability’ from https://cwe.mitre.org for each vulnerability 
    3. Print list of vulnerabilities with severity High or above AND ‘Likelihood of exploitability’ High or above 

#########
Fetch all code scanning alerts for above repo with severity High or above
########

There are two ways one with filter using query like this 
#url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/code-scanning/alerts?q=is:severity:{min_severity}..critical" 
but this didn't worked for some reason so i moved to anyother API

Second method is    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/code-scanning/alerts?severity={severity}"
in this we pass the severity and it replies back with alerts for particular repo.

Flow:-
main() - starting point
get_alerts_severity() - kind of doing job of main , calling below methods for each alert severity
    fetch_alerts() - this method does API call to get alerts for a repo
id_conversion_to_url_cwe() - we get CWE-184 but the URL is https://cwe.mitre.org/data/definitions/184.html so we need 184 out of CWE-184
    handle_two_digit_cwe() - we get CWE-098 but URL is https://cwe.mitre.org/data/definitions/98.html so we need 98 out of CWE-098
get_exploitability_from_html()
    now once we have URL we get likelihood of exploit
"""


# Replace with your actual values
token="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"
github_token = token
repo_owner = "mkpmanish"
repo_name = "django_vulnerable_app"
min_severity = "high"  # Fetch alerts with severity "high" or above
cwe_base_url = "https://cwe.mitre.org/data/definitions/"

cwe_base_url = "https://cwe.mitre.org/data/definitions/"

def handle_two_digit_cwe(cwe_id):
    """
    The CWE-ID = CWE-016 but URL is https://cwe.mitre.org/data/definitions/16.html
    so, we need to transform CWE-016 to 16.html
    :param cwe_id: CWE-098
    :return:
    """
    parts_cwe_id = cwe_id.split('-')
    new_cwe_id = parts_cwe_id[1]
    if parts_cwe_id[1].startswith("0"):
        new_cwe_id = parts_cwe_id[1][1:]
    return new_cwe_id
def id_conversion_to_url_cwe(cwe_id):
    """
    parse out CWE-116 and get 116 , get number out of CWE-ID
    :param cwe_id:
    :return:
    """
    new_cwe_id = cwe_id
    if cwe_id.startswith("external"):
        cwe_split = cwe_id.split('/')
        id = cwe_split[2]
        if '0' in id:
            new_cwe_id = handle_two_digit_cwe(cwe_id)
        else:
            new_cwe_id = id.split('-')[1]
    return(new_cwe_id)


def fetch_alerts(url, headers):
    """
    Request to github to get alerts https://api.github.com/repos/{repo_owner}/{repo_name}/code-scanning/alerts?severity={severity}

    :param url: URL of alerts
    :param headers: auth headers
    :return:
    """
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error retrieving alerts: {response.status_code}")
        return []

def get_exploitability(cwe_id):
    """
    create URL and get severity
    :param cwe_id:
    :return:
    """
    url = urljoin(cwe_base_url, f"{cwe_id}.html")
    severity = get_exploitability_from_html(url)
    return severity


def get_exploitability_from_html(url):
    """
    hit CWE and get likelihood_of_exploit

    :param url:
    :return:
    """
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        try:
            div_with_id = soup.find('div', id="Likelihood_Of_Exploit")
            text_inside_div = div_with_id.text.strip()
            header_on_html_page = "Likelihood Of Exploit"
            severity = text_inside_div[len(header_on_html_page):]
        except:
            severity = ""
        return(severity)
    else:
        print(f"Error retrieving HTML content: {response.status_code}")
    return "Unknown"


def get_alerts_severity(severity):
    """
    Step by Step flow:-
        1. check if github token is present
        2. Call Alerts api to get alerts for particular severity
        3. Loop over each alert and parse details like severity, alert number, likelihood of exploit, Name
        4. convert eg. CWE-114 into 114.html
        5. create URL and get likelihood_of_exploit from URL
        6. set final likelihood_of_exploit , pick the highest
        7. Final print of alert with High/Critical exploitibility and severity

    :param severity:
    :return: none
    :print : severity, alert number, likelihood, Rule-Name
    """
    #check if github token is present
    if not github_token:
        print("Error: Missing GITHUB_ACCESS_TOKEN is not configured")
        return
    headers = {"Authorization": f"token {github_token}"}

    #Call Alerts api to get alerts for particular severity
    #https://gist.github.com/bonniss/4f0de4f599708c5268134225dda003e0
    #url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/code-scanning/alerts?q=is:severity:{min_severity}..critical"
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/code-scanning/alerts?severity={severity}"
    alerts = fetch_alerts(url, headers)

    # Loop over each alert
    for alert in alerts:
        #print(alert['number'])
        cwe_id = alert.get("rule", {}).get("tags")
        try:
            cwe_id.remove("security")
            cwe_id.remove("correctness")
        except:
            pass
        if len(cwe_id) >= 1:
            high_exploitability_alerts = []
            for each_cwe in cwe_id:
                if each_cwe.startswith("external"):
                    # convert CWE-114 into 114.html
                    cwe_id_value = id_conversion_to_url_cwe(each_cwe)
                    url  = "https://cwe.mitre.org/data/definitions/" + cwe_id_value +".html"
                    # create URL and get likelihood_of_exploit from URL
                    high_exploitability_alerts.append(get_exploitability_from_html(url))
                else:
                    pass
                    #print("Not a URL to be analysed")
            exploitability = ""

            #set final likelihood_of_exploit , pick the highest
            if 'High' in high_exploitability_alerts:
                exploitability = "High"
            if 'Medium' in high_exploitability_alerts:
                exploitability = "Medium"
            if 'Low' in high_exploitability_alerts:
                exploitability = "Low"
            if 'Informational' in high_exploitability_alerts:
                exploitability = "Informational"

            # Final print of alert with High/Critical exploitibility and severity
            if exploitability == "High" or exploitability == "Critical" :
                print("Vulnerability Severity --> "+severity, ",Alert Number --> " + str(alert['number']), "Likelihood of Exploit --> "+exploitability, ",Rule-Name -->" + alert['rule']['name'])
            else:
                pass
                #print("This vulnerabilities is not with High Severity and High Likelihood of Exploitability.")

def main():
    """
    uncomment to get all alerts from CodeQL
    :return:
    """
    get_alerts_severity("high")
    get_alerts_severity("critical")
    #get_alerts_severity("medium")
    #get_alerts_severity("low")

if __name__ == "__main__":
    main()
