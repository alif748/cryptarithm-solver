// const url = 'http://localhost:5009/cryptarithm'
const url = 'https://api3.alifm.net/cryptarithm'

function addVariable() {
    const inputPlace = document.querySelector('#input-place')
    if (inputPlace.children.length < 4) {
        // Create the new elements
        const pElement = document.createElement('p')
        pElement.classList.add('h-12', 'my-3')

        const inputElement = document.createElement('input')
        inputElement.type = 'text'
        inputElement.classList.add('h-12', 'p-3', 'text-right', 'leading-7', 'tracking-extraWide', 'uppercase', 'left')
        inputElement.maxLength = 10
        inputElement.placeholder = 'Input..'

        // Append the input element to the p element
        pElement.appendChild(inputElement)

        // Append the p element to the input place container
        inputPlace.appendChild(pElement)
    } else {
        alert("You can only add 4 variables")
    }
}

function reload() {
    window.location.reload()
}

async function go() {
    btnLoading()
    const op = document.querySelector('#op').value
    const right = document.querySelector('#right').value

    const inputPlaces = document.querySelectorAll('.left')
    let leftRaw = []
    inputPlaces.forEach(x => {
        if (x.value) {
            leftRaw.push(x.value)
        }
    })

    if (leftRaw.length > 1 && right) {
        const left = leftRaw.join(',')

        console.log(left)
        console.log('Right: ' + right)

        try {
            const response = await axios.post(url, {
                input: left,
                res: right,
                op: op,
            })

            const { data } = response
            let resLeft = ''

            data.left.forEach(x => {
                console.log(x)

                resLeft += `
                    <p class="h-12 my-3 text-right leading-7 tracking-extraWide uppercase">
                        ${x}
                    </p>
                `
            })

            document.querySelector('#result').innerHTML = `
                <table class="table-fixed text-right text-3xl">
                    <tr>
                        <td class="text-center mx-5">${data.operation}</td>
                        <td class="w-40">
                            <div id="input-place">
                                ${resLeft}
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td class="border-t-4 border-transparent"></td>
                        <td class="border-t-4 border-slate-900">
                            <p class="h-12 my-3 text-right leading-7 tracking-extraWide uppercase">
                                ${data.right}
                            </p>
                        </td>
                    </tr>
                </table>
            `

            const json = data.mapping
            const tableContainer = document.querySelector('#result2')
            const table = document.createElement('table')
            table.classList.add('table-auto', 'border-collapse', 'border', 'border-gray-200')
            const thead = document.createElement('thead')
            thead.classList.add('bg-gray-50')
            const tbody = document.createElement('tbody')
            const keyRow = document.createElement('tr')
            const valueRow = document.createElement('tr')

            for (const key in json) {
                const keyCell = document.createElement('td')
                keyCell.classList.add('border', 'border-gray-800', 'px-3', 'py-2', 'text-3xl', 'font-medium', 'text-gray-900', 'bg-white', 'text-center')
                keyCell.textContent = key
                keyRow.appendChild(keyCell)

                const valueCell = document.createElement('td')
                valueCell.classList.add('border', 'border-gray-800', 'px-3', 'py-2', 'text-3xl', 'text-gray-900', 'bg-white', 'text-center')
                valueCell.textContent = json[key]
                valueRow.appendChild(valueCell)
            }

            tbody.appendChild(keyRow)
            tbody.appendChild(valueRow)
            table.appendChild(tbody)
            tableContainer.appendChild(table)
            document.querySelector('#time').innerHTML = `
            <p class='my-10'>
                Execution time: ${data.execution_time} second
            </p>
            `

            btnLoaded()
        } catch (e) {
            btnLoaded()
            if (e.response && e.response.status == 404) {
                document.querySelector('#result').innerHTML = `
                    <div class="text-center text-red-600 text-2xl">
                        ${e.response.data.message}
                    </div>
                `
            } else {
                console.log(e)
            }
        }
    } else {
        alert('Please fill in the input area.')
        btnLoaded()
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const inputElement = document.querySelector('#right')

    inputElement.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            go();
        }
    });
});

function btnLoading() {
    document.getElementById('btn-first').classList.add('hidden')
    document.getElementById('btn-loading').classList.remove('hidden')
    document.getElementById('btn-loading').classList.add('inline-flex')
    console.log('loading')
    document.querySelector('#result').innerHTML = ''
    document.querySelector('#result').classList.remove('mt-48')
    document.querySelector('#result2').innerHTML = ''
    document.querySelector('#result2').classList.remove('mt-48')
    document.querySelector('#time').innerHTML = ''
    document.querySelector('#time').classList.remove('mt-48')
}

function btnLoaded(stat) {
    document.getElementById('btn-first').classList.remove('hidden')
    document.getElementById('btn-loading').classList.add('hidden')
    document.getElementById('btn-loading').classList.remove('inline-flex')
    console.log('loaded')
    if (stat == 'yes') {
        document.querySelector('#result').classList.add('mt-48')
        document.querySelector('#result2').classList.add('mt-48')
    }
    setTimeout(function () {
        window.scrollTo({
            top: document.querySelector('#result').offsetTop - 20,
            left: 0,
        })
    }, 600)
}
