import hashlib
import json
import copy
from datetime import datetime as date
from flask import Flask, render_template, request, redirect


class Block:
    def __init__(self, index, timestamp, data, previous_hash,hash=''):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        if hash == '':
            self.hash = self.generate_hash()
        else:
            self.hash=hash

    def generate_hash(self):
        sha = hashlib.sha256()
        sha.update(
            str(self.index).encode('utf-8') +
            str(self.timestamp).encode('utf-8') +
            str(self.data).encode('utf-8') +
            str(self.previous_hash).encode('utf-8')
        )
        return sha.hexdigest()


class BlockChain():
    def __init__(self):
        self.blocks = []
        self.dataList = []
        self.prev_block = None
        self.generate_genesis_block()

    def create_dataList(self, from_address, whom, lotto_number, duedate):
        self.dataList.append({
            'from_address': from_address,
            'whom': whom,
            'lotto_number': lotto_number,
            'duedate': duedate,
        })

    def generate_genesis_block(self):
        block = Block(0, date.now(), "Genesis block", "0")
        self.blocks.append(block)
        self.prev_block = block

    def generate_next_block(self):
        this_index = self.prev_block.index + 1
        this_date = date.now()
        previous_hash = self.prev_block.hash
        block = Block(this_index, this_date, self.dataList, previous_hash)
        self.dataList = []
        self.blocks.append(block)
        self.prev_block = block
    
    def isChainValid(self):
        self.editId = []
        for index in range(1,len(self.blocks)):
            currb=Block(self.blocks[index].index ,
                        self.blocks[index].timestamp ,
                        self.blocks[index].data ,
                        self.blocks[index].previous_hash ,
                        self.blocks[index].hash)
            prevb=Block(self.blocks[index-1].index ,
                        self.blocks[index-1].timestamp ,
                        self.blocks[index-1].data ,
                        self.blocks[index-1].previous_hash ,
                        self.blocks[index-1].hash)
            if currb.hash != currb.generate_hash():
                self.editId.append(index)
            if currb.previous_hash != prevb.hash:
                self.editId.append(index)
        
        if len(self.editId) == 0:
            return "isChainValid"
        else:
            return self.editId


# -V2 run blockchain in web
blockchain = BlockChain()
blockchain.create_dataList("Familymart", "Boss", "123456", "16/12/2562")
blockchain.generate_next_block()
blockchain.create_dataList("Familymart", "Leo", "999999", "16/12/2562")
blockchain.generate_next_block()
blockchain.create_dataList("Familymart", "Toei", "000000", "16/12/2562")
blockchain.generate_next_block()
blockchain.create_dataList("Familymart", "Leo", "999987", "16/12/2562")
blockchain.generate_next_block()
blockchain.create_dataList("Familymart", "Boss", "123456", "16/12/2562")
blockchain.generate_next_block()
blockchain.create_dataList("Familymart", "Leo", "999999", "16/12/2562")
blockchain.generate_next_block()
blockchain.create_dataList("Familymart", "Toei", "000000", "16/12/2562")
blockchain.generate_next_block()
blockchain.create_dataList("Familymart", "Leo", "999987", "16/12/2562")
blockchain.generate_next_block()
blockchain.create_dataList("Familymart", "Toei", "000000", "16/12/2562")
blockchain.generate_next_block()
blockchain.create_dataList("Familymart", "Leo", "999987", "16/12/2562")
blockchain.generate_next_block()


app = Flask(__name__)


@app.route('/newBlock/', methods=['POST'])
def new_Block():
    blockchain.create_dataList(
        request.form['from_address'], request.form['whom'], request.form['lotto_number'], request.form['duedate'])
    blockchain.generate_next_block()
    return redirect("http://localhost:8080/blocks")


@app.route('/editBlock/',methods=['POST'])
def edit_Block():
    blockchain.blocks[int(request.form['editIndex'])].data[0]['from_address'] = request.form['editFrom_address']
    blockchain.blocks[int(request.form['editIndex'])].data[0]['whom'] = request.form['editWhom']
    blockchain.blocks[int(request.form['editIndex'])].data[0]['lotto_number'] = request.form['editLotto_number']
    blockchain.blocks[int(request.form['editIndex'])].data[0]['duedate'] = request.form['editDuedate']
    return redirect("http://localhost:8080/")

@app.route("/addnewblock")
def viewAddnewblock():
    return render_template('addnewblock.html', blocks=blockchain.blocks)


@app.route("/blocks")
def viewBlocks():
    return render_template('blocks.html', blocks=blockchain.blocks,isChainValid=blockchain.isChainValid())


@app.route("/")
def viewIndex():
    return render_template('index.html', blocks=blockchain.blocks)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
