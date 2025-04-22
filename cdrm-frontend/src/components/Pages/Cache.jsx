import React, { useState, useEffect, useRef } from 'react';

function Cache() {
  const [searchQuery, setSearchQuery] = useState('');
  const [cacheData, setCacheData] = useState([]);
  const [keyCount, setKeyCount] = useState(0);
  const debounceTimeout = useRef(null); // ← store the timeout ID

  const handleInputChange = (event) => {
    const query = event.target.value;
    setSearchQuery(query);

    // Clear the previous timeout
    if (debounceTimeout.current) {
      clearTimeout(debounceTimeout.current);
    }

    // Set a new timeout
    debounceTimeout.current = setTimeout(() => {
      if (query.trim() !== '') {
        sendApiCall(query);
      } else {
        setCacheData([]); // optional: clear results on empty query
      }
    }, 1000); // 2 seconds
  };

  const fetchKeyCount = () => {
    fetch('/api/cache/keycount')
      .then((response) => response.json())
      .then((data) => {
        setKeyCount(data.count);
      })
      .catch((error) => {
        console.error('Error fetching key count:', error);
      });
  };

  useEffect(() => {
    const fetchInterval = setInterval(fetchKeyCount, 10000);
    fetchKeyCount();
    return () => clearInterval(fetchInterval);
  }, []);

  const sendApiCall = (text) => {
    fetch('/api/cache/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ input: text }),
    })
      .then((response) => response.json())
      .then((data) => setCacheData(data))
      .catch((error) => console.error('Error:', error));
  };


  return (
    <>
      <div className='w-full h-full bg-zinc-900 flex flex-col p-0'>
        <div className='flex flex-row w-full'>
          <form className='flex flex-row w-8/10 p-10 h-full rounded-xl self-start'>
            <input
              type='text'
              id='search'
              name='search'
              value={searchQuery}
              onChange={handleInputChange}
              placeholder='Search by PSSH/KID'
              className='w-full text-white bg-[rgba(0,0,0,0.2)] focus:outline-none rounded focus:shadow-sm focus:shadow-green-700/50 transition-shadow duration-300 ease-in-out p-2'
            />
          </form>
          <p className='text-white w-2/10 p-10 rounded-xl self-start flex flex-col h-full'>
            <span className='text-white w-1/1 text-center'>
              Cached Keys: {keyCount} {/* Display the count of cached keys */}
            </span>
          <a href='/api/cache/download'>
          <button className=' self-start w-1/1 bg-green-700 rounded-md mt-1 active:transform active:scale-95 cursor-pointer hover:bg-green-600/50 pt-1 pb-1'>
            Download
          </button>
          </a>
          </p>
        </div>
        <div className='h-full w-full p-10 overflow-y-auto'>
          <div className="overflow-x-auto border p-10 rounded-2xl bg-[rgba(0,0,0,0.2)] shadow-md shadow-green-700 min-h-full overflow-y-auto">
            <table className='min-w-full text-white'>
              <thead>
                <tr>
                  <th className='p-2 border border-black'>PSSH</th>
                  <th className='p-2 border border-black'>KID</th>
                  <th className='p-2 border border-black'>Key</th>
                </tr>
              </thead>
              <tbody>
                {cacheData.length > 0 ? (
                  cacheData.map((item, index) => (
                    <tr key={index}>
                      <td className='p-2 border border-black'>{item.PSSH}</td>
                      <td className='p-2 border border-black'>{item.KID}</td>
                      <td className='p-2 border border-black'>{item.Key}</td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="3" className='p-2 border  border-black text-center'>
                      No data found
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </>
  );
}

export default Cache;
