import MySQLdb as db
import json
import requests
import solr
import crawl

s = solr.SolrConnection('http://10.139.243.107:8983/solr')

def main():
    response = s.query('id:*BoschProductDetail.aspx?pid=*', rows=300)
#     print response.len
    pid = []
    for hit in response.results:
        pid.append(hit['id'].split('=')[1])
        # pid = []
        # pid.append(hit['id'].split('=')[1])

        # print pid
        # details=crawl.getpidinfo(pid)

    details=crawl.getpidinfo(pid)
    for detail in details:
        detail['category'] = getCategory(detail['category'])
        insertProduct(detail)
    return

def getCategory(catid):
    response = s.query('id:*catid='+ str(catid)+'*', rows=1)
#     print response.len
    for hit in response.results:
        category =  hit['title'].split('|')[0]
        print category
        return category

def insertReview(review):
    con = db.connect('10.5.18.67','12CS30026','dual12','12CS30026');

    with con:
        cur = con.cursor()
        query = "INSERT INTO Review(pid,title, text, nick, date, sentiment_score) VALUES("\
                + '"' + review['pid']    + '", '\
                + '"' + review['title']         + '", '\
                + '"' + review['text']         + '", '\
                + '"' + review['nick']         + '", '\
                + '"' + review['date']         + '", '\
                + " NULL "\
                + ")";\
        print query
        cur.execute(query)
    return

def insertProduct(product):
    con = db.connect('10.5.18.67', '12CS30026','dual12','12CS30026');

    with con:
        cur = con.cursor()
        query = "INSERT INTO Product(pid,pname ,plink ,rating ,description ,category) VALUES("\
                +'"'+ product['pid']           + '", '\
                +'"'+ product['pname']             + '", '\
                +'"'+ product['plink']             + '", '\
                +'"'+ product['rating']         + '", '\
                +'"'+ product['description'] + '", '\
                +'"'+ product['category']         + '"'\
                + ")";\
        print query
        cur.execute(query)

    for review in product['reviews']:
        insertReview(review)
    return


if __name__=='__main__':
    main()