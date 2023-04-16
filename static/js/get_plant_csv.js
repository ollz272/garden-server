function setCsvUrl(baseUrl) {
    const start = document.getElementById("id_start_date").value
    const end = document.getElementById("id_end_date").value
    const periodResolution = document.getElementById("id_resolution").value
    url = baseUrl + `?period_resolution=${periodResolution}&start=${start}&end=${end}`
    var download_link = document.getElementById("download_data_link_id")
    download_link.href = url
}

url = document.currentScript.getAttribute('url')
setCsvUrl(url)