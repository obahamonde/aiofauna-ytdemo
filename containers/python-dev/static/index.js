const $ = (selector) => document.querySelector(selector)

const app = $("#app")

app.innerHTML = `
    <h1>Hello World!</h1>
`