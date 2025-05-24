import axios from "axios";
import * as cheerio from "cheerio";
import * as fs from "fs";

const PATH_TO_PHISING_URLS: string = "https://raw.githubusercontent.com/openphish/public_feed/refs/heads/main/feed.txt";
const TIME_TODAY = new Date().toISOString().split("T")[0] as string;
const PATH_TO_JSON_FILE: string = `${TIME_TODAY}_phishing_urls.json`;
const USER_AGENT: {[key: string]: string} = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
};

type PhishingEmails = {
    "Url": string,
    "Posted": string,
    "Title": string,
    "HTML": string
};

const openJSONFile = (path_to_file: string): object => {
    const json_file: string = fs.readFileSync(path_to_file, "utf-8");
    const result: object = JSON.parse(json_file);
    return result;
};

const fetchData = async (path_to_url: string, user_agent: {[key: string]: string}): Promise<PhishingEmails> => {
    try {
        const resp = await axios.get(path_to_url, {user_agent});
        const selector = cheerio.load(resp.data);
        let result: PhishingEmails = {
        "Url": path_to_url,
        "Posted": TIME_TODAY,
        "Title": selector("title").text(),
        "HTML": resp.data
        };
        return result;
    }
    catch (err) {
        console.log(`Couldn't fetch ${path_to_url}`)
    }
};

const writeToJSON = (path_to_file: string, data: string): void => {
    fs.writeFile(path_to_file, JSON.stringify(data), (err) => {
        if (err) throw err;
        }
    )
};

const runAll = async () => {
    const response = await axios.get(PATH_TO_PHISING_URLS);
    const new_urls: string[] = response.data.split("\n");
    // let stored_urls: any = openJSONFile(PATH_TO_JSON_FILE);
    let result: any = [];
    for (let new_url of new_urls) {
        let new_entry: PhishingEmails = await fetchData(new_url, USER_AGENT);
        result.push(new_entry);
    }
    writeToJSON(PATH_TO_JSON_FILE, result);
};

runAll();