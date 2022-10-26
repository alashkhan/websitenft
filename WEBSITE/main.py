from flask import Flask, request
import requests
import psycopg2


app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")


@app.route('/Information', methods=['GET', 'POST'])
def Information():
    if request.method == 'POST':
        address = request.form.get('address')
        url = 'https://solana-gateway.moralis.io/nft/mainnet/' + address + '/metadata'
        headers = {
            "accept": "application/json",
            "X-API-Key": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
        }
        response = requests.get(url, headers=headers)
        print(response.text)


        conn = psycopg2.connect(
            database="solana", user='postgres', password='1234', host='localhost', port='5432'
        )

        cursor = conn.cursor()


        create_script = ''' CREATE TABLE IF NOT EXISTS NFT
(
  name VARCHAR(200),
  address VARCHAR(1000))'''

        cursor.execute(create_script)

        insert_script = "INSERT INTO solana (name, address) VALUES (%s, %s)"
        insert_value = ("solana name", response.text)

        cursor.execute(insert_script, insert_value)

        conn.commit()

        conn.close()

        return '''
                  <h1>NFT's info: {}</h1>'''.format(response.text)
    return '''
          


if __name__ == '__main__':
    app.run(debug=True, port=5000)
e
