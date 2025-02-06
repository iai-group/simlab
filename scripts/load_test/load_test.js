// k6 installation: https://grafana.com/docs/k6/latest/set-up/install-k6/
// k6 running: k6 run load_test.js --insecure
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Trend } from 'k6/metrics';

const uploadImageTrend = new Trend('upload_image_duration');

export let options = {
    stages: [
        { duration: '30s', target: 10 },  // Ramp-up to 10 users
        { duration: '1m', target: 50 },   // Load test with 50 users
        { duration: '30s', target: 100 }, // Stress test with 100 users
        { duration: '30s', target: 0 }    // Ramp-down
    ],
};

export default function () {
    let base_url = 'https://34.121.140.186';

    // Authentication cookies
    let authHeaders = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'multipart/form-data',
        'Cookie': 'remember_token=67a3d609a5f8bcb68fa4ac8f|ea5637712c47a51d3c172e723946a7371642a0252fc23d848fc7a854c40028c9994d2d41c492392791d8187825c1bafa4cfec1d2988f683eba87134991256706; session=.eJwlzjsOwjAMANC7ZGZw_EnsXqZynFiwtnRC3J1KzG95n7Lnsc5n2d7HtR5lf82yFc5wFkeSlhNJM4ExDW0qDSBm4fBKfUWTiUox15izqztF12Cx5hwAy0cdVWvVjp0hUFhuDWMX6qDg7YaUNdCommmNgGxR7sh1ruO_ad1pNjCX1BGjaTp7aJbvDxrlNW0.Z6PWEg.bXQQXGJyQjMfQn16NVAdRceTtfg',
        'Origin': base_url,
        'Referer': `${base_url}/system`,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    };

    
    let experimentRes = http.get(`${base_url}/experiment`, { headers: authHeaders });
    check(experimentRes, {
        'experiment status is 200': (r) => r.status === 200,
    });

    let systemRes = http.get(`${base_url}/system`, { headers: authHeaders });
    check(systemRes, {
        'system status is 200': (r) => r.status === 200,
    });

    
    let tarFile = open('testtar.tar', 'b'); 
    let formData = {
        file: http.file(tarFile, 'testtar.tar', 'application/x-tar'),
        image_name: 'testing'
    };

    let uploadRes = http.post(`${base_url}/api/upload-image`, formData, { headers: authHeaders });
    uploadImageTrend.add(uploadRes.timings.duration);

    check(uploadRes, {
        'upload image status is 202 accepted': (r) => r.status === 202,
        'upload image completed within 2s': (r) => r.timings.duration < 2000,
    });

    sleep(1); 
}
