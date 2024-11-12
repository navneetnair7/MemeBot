"use client";

import React, { useState } from 'react';
import axios from 'react';
import { Search, Upload } from 'lucide-react';

const MemeSearchPage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [memes, setMemes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      const response = await axios.get(`https://localhost:5000/seaerch?q=${searchQuery}`);
      setMemes(response.data.memes);
    } catch (err) {
      setError('Failed to fetch memes. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleMemeUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('meme', file);

    try {
      await axios.post('/api/upload/meme', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setSuccess('Meme uploaded successfully!');
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError('Failed to upload meme. Please try again.');
    }
  };

  const handleDatasetUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('dataset', file);

    try {
      await axios.post('/api/upload/dataset', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setSuccess('Dataset uploaded successfully!');
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError('Failed to upload dataset. Please try again.');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-violet-900 p-8 text-white">
      {/* Top Bar */}
      <div className="flex justify-between mb-12">
        <div className="relative">
          <input
            type="file"
            onChange={handleDatasetUpload}
            className="hidden"
            id="dataset-upload"
            accept=".csv,.json"
          />
          <label
            htmlFor="dataset-upload"
            className="flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors duration-200 cursor-pointer backdrop-blur-sm bg-opacity-50"
          >
            <Upload size={20} />
            Upload Dataset
          </label>
        </div>

        <div className="relative">
          <input
            type="file"
            onChange={handleMemeUpload}
            className="hidden"
            id="meme-upload"
            accept="image/*"
          />
          <label
            htmlFor="meme-upload"
            className="flex items-center gap-2 px-4 py-2 bg-violet-600 text-white rounded-lg hover:bg-violet-700 transition-colors duration-200 cursor-pointer backdrop-blur-sm bg-opacity-50"
          >
            <Upload size={20} />
            Upload Meme
          </label>
        </div>
      </div>

      {/* Search Section */}
      <div className="max-w-2xl mx-auto mb-12">
        <form onSubmit={handleSearch} className="relative">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search for memes..."
            className="w-full px-4 py-3 pr-12 rounded-lg bg-gray-800 border border-gray-700 focus:outline-none focus:border-purple-500 text-white placeholder-gray-400"
          />
          <button
            type="submit"
            className="absolute right-3 top-1/2 -translate-y-1/2"
          >
            <Search className="text-gray-400 hover:text-purple-400 transition-colors duration-200" />
          </button>
        </form>
      </div>

      {/* Status Messages */}
      {error && (
        <div className="mb-4 text-center text-red-400">
          {error}
        </div>
      )}
      
      {success && (
        <div className="mb-4 text-center text-green-400">
          {success}
        </div>
      )}

      {/* Results Grid */}
      {loading ? (
        <div className="text-center text-purple-200">Loading...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {memes.map((meme, index) => (
            <div key={index} className="bg-gray-800 bg-opacity-50 rounded-lg shadow-xl overflow-hidden backdrop-blur-sm border border-gray-700 hover:border-purple-500 transition-colors duration-200">
              <img
                src={meme.url}
                alt={meme.title || 'Meme'}
                className="w-full h-64 object-cover"
              />
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default MemeSearchPage;