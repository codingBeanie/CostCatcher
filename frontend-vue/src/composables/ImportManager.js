import { modal } from './Modal.js'
import { toast } from './Toast.js' 


export async function sendData(rawData, selectFirst, selectLast, selectDate, selectRecipient, selectDescription, selectAmount) {
    const data = createDataFrame(rawData, selectFirst, selectLast, selectDate, selectRecipient, selectDescription, selectAmount)
    const undefined = checkUndefined(data)

    // handle messages
    if (undefined.result === false) {
        let index = undefined.index + selectFirst.value
        const prompt = await modal('Error', `Data is missing in row ${index}`, true, true)
        console.log("PROMPT",prompt)
    }
}


// creating data frame
function createDataFrame(rawData, selectFirst, selectLast, selectDate, selectRecipient, selectDescription, selectAmount) {
    const data = {}
    var dataIndex = 0
    // create Data object for transmission
    rawData.forEach((line, index) => {
        if (index + 1 >= selectFirst.value && index + 1 <= selectLast.value) {
            data[dataIndex] = {
                date: line[selectDate.value - 1],
                recipient: line[selectRecipient.value - 1],
                description: line[selectDescription.value - 1],
                amount: line[selectAmount.value - 1]
            }
            dataIndex++
        }

    })

    // check data and create message
    return data 
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

