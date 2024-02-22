import { modal } from './Modal.js'
import { toast } from './Toast.js' 
import { postData } from '../composables/API.js'

export async function sendData(rawData, selectFirst, selectLast, selectDate, selectRecipient, selectDescription, selectAmount) {
    const data = createDataFrame(rawData, selectFirst, selectLast, selectDate, selectRecipient, selectDescription, selectAmount)
    const undefined = checkUndefined(data)

    // handle messages
    if (undefined.result === false) {
        let index = undefined.index + selectFirst.value
        const prompt = await modal('Error', `Data is missing in row ${index}`, true, true)
        if (prompt === true) {
            postData(data, "transactions")
            toast('Data was sent')
        }
        else {
            toast('Data was not sent')
        }
    }
    else {
        postData(data, 'transactions')
        toast('Data was sent')
    }
}


// creating data frame
function createDataFrame(rawData, selectFirst, selectLast, selectDate, selectRecipient, selectDescription, selectAmount) {
    const fileName = document.getElementById('inputFile').files[0].name.split('.')[0]
    var dataArray = []
    const sourceFileDate = new Date()
    // create Data object for transmission
    rawData.forEach((line, index) => {
        if (index + 1 >= selectFirst.value && index + 1 <= selectLast.value) {
            const [day, month, year] = line[selectDate.value - 1].split('.')
            const amount = parseFloat(line[selectAmount.value - 1].replace('.', '').replace(',', '.'))

            var data = {
                date: year + '-' + month + '-' + day,
                sourceFile: fileName,
                sourceFileDate: sourceFileDate,
                recipient: line[selectRecipient.value - 1],
                description: line[selectDescription.value - 1],
                amount: amount
            }
            dataArray.push(data)
        }

    })

    // check data and create message
    return dataArray 
}

// checking data validity
function checkUndefined(data) {
    
    for (let [index, value] of Object.entries(data)) {
        for (let element of Object.entries(value)) {
            if (element[1] === undefined) {
                return {result: false, index: index}
            }
        }
    }
    return {result: true}
}

