import { BiLoaderAlt } from 'react-icons/bi';
import React, { useState, useEffect } from 'react'
import axios from 'axios';

const style = {
  main: "min-h-screen h-full bg-black/10 dark:bg-black/20",
  container: "h-fit py-32 pb-16 flex flex-col md:flex-col items-center md:justify-between h-full px-16 sm:px-44",
  heading: "text-[min(7.5vw,2.2rem)] font-bold mb-4 sm:mb-8 text-black dark:text-white",
  subheading: "text-[max(1.5vw,1rem)] font-medium mb-6 text-black w-full mt-16 dark:text-white",
  input: "w-full bg-red-200 text-black b-2 border-black/20 rounded-full py-2 px-4 sm:px-8 text-[max(1vw,0.8rem)] font-medium focus:outline-none focus:ring-2 focus:ring-red-400 focus:border-transparent transition duration-300 ease-in-out",
  button: "my-4 bg-yellow-400 text-red-500 font-medium text-[max(1vw,0.8rem)] py-2 px-4 sm:px-8 rounded-full hover:bg-yellow-500 hover:text-white transition duration-300 ease-in-out",
  outputsection: "w-full",
  hide: "",
  outbox: "w-full bg-black/10 mt-2 p-4 dark:bg-black",
  data: "dark:text-green/50"
}

const HeroSection = () => {
  const [query, setQuery] = useState('');
  const [out, setOut] = useState<any>();
  const [outputRaw, setOutputRaw] = useState<any>();
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingPDF, setIsLoadingPDF] = useState(false);

  const generatePoem = async (query: string) => {
    const url = "https://poemgeneratorwithtopic.onrender.com/get_poem_raw/";
    axios.defaults.headers.post["Content-Type"] =
      "application/json;charset=utf-8";
    axios.defaults.headers.post["Bypass-Tunnel-Reminder"] = "1";
    axios.defaults.headers.post["Access-Control-Allow-Origin"] = "*";
    try {
      const { data } = await axios.post(
        url,
        { "query": query }
      );
      setOut(
        <div className={style.data} dangerouslySetInnerHTML={{ __html: data.html_output }}></div>
      );
      setOutputRaw(data.output);
    } catch (error) {
      console.error(error);
    }
  }

  const generatePDF = async (query: string, output: string) => {
    const url = "https://poemgeneratorwithtopic.onrender.com/poem_pdf_maker/";
    axios.defaults.headers.post["Content-Type"] =
      "application/json;charset=utf-8";
    axios.defaults.headers.post["Bypass-Tunnel-Reminder"] = "1";
    axios.defaults.headers.post["Access-Control-Allow-Origin"] = "*";
    try {
      const { data } = await axios.post(
        url,
        {
          "query": query,
          "output": output,
        },
        { responseType: 'blob' } // Set the response type to blob
      );
      const pdfUrl = URL.createObjectURL(new Blob([data], { type: 'application/pdf' }));
      window.open(pdfUrl, '_blank'); // Open the PDF in a new tab
    } catch (error) {
      console.error(error);
    }
  }

  const handleTopicChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(event.target.value);
  };

  const handleGenerateClick = async () => {
    console.log(JSON.stringify(query))
    if (query !== '') {
      setIsLoading(true);
      await generatePoem(query);
      setIsLoading(false);
    }
  };

  const handleDownloadClick = async () => {
    if (outputRaw !== '') {
      setIsLoadingPDF(true);
      await generatePDF(query, outputRaw);
      setIsLoadingPDF(false);
    }
  };


  return (
    <>
      <div className={style.main}>
        <div className={style.container}>
          <h1 className={style.heading}>Enter a Topic to Generate Poem</h1>
          <input
            type="text"
            value={query}
            onChange={handleTopicChange}
            className={style.input}
            placeholder='Enter a Topic'
          />
          <button
            className={style.button}
            onClick={handleGenerateClick}
          >
            {isLoading ? (
              <div className="animate-spin">
                <BiLoaderAlt />
              </div>
            ) : (
              'Generate'
            )}
          </button>

          {out ? (
            <div className={`${style.outputsection}`}>
              <div className={style.subheading}>
                Output:
              </div>
              <div className={style.outbox}>
                {out}
              </div>
              <button
                className={style.button}
                onClick={handleDownloadClick}
              >
                {isLoadingPDF ? (
                  <div className="animate-spin">
                    <BiLoaderAlt />
                  </div>
                ) : (
                  'Download PDF'
                )}
              </button>
            </div>
          ) : (
            <div className={style.hide}>Generate to See Output</div>
          )}
        </div>
      </div>
    </>
  );
}

export default HeroSection