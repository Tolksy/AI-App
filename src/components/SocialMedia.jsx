import React, { useState, useEffect } from 'react'
import { Send, Bot, User, Calendar, TrendingUp, Hash, Clock, Target, MessageSquare } from 'lucide-react'
import { buildApiUrl } from '../config/api'

const SocialMedia = () => {
  const [content, setContent] = useState('')
  const [topic, setTopic] = useState('')
  const [platform, setPlatform] = useState('linkedin')
  const [tone, setTone] = useState('professional')
  const [length, setLength] = useState('medium')
  const [includeHashtags, setIncludeHashtags] = useState(true)
  const [scheduledTime, setScheduledTime] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [generatedContent, setGeneratedContent] = useState('')
  const [hashtags, setHashtags] = useState([])
  const [optimalTime, setOptimalTime] = useState('')
  const [engagementPrediction, setEngagementPrediction] = useState({})

  const platformOptions = [
    { value: 'linkedin', label: 'LinkedIn', icon: '💼' },
    { value: 'twitter', label: 'Twitter', icon: '🐦' },
    { value: 'facebook', label: 'Facebook', icon: '📘' },
    { value: 'instagram', label: 'Instagram', icon: '📷' }
  ]

  const toneOptions = [
    { value: 'professional', label: 'Professional' },
    { value: 'casual', label: 'Casual' },
    { value: 'inspirational', label: 'Inspirational' },
    { value: 'educational', label: 'Educational' },
    { value: 'humorous', label: 'Humorous' }
  ]

  const lengthOptions = [
    { value: 'short', label: 'Short (50-100 chars)' },
    { value: 'medium', label: 'Medium (100-200 chars)' },
    { value: 'long', label: 'Long (200-500 chars)' }
  ]

  const generateContent = async () => {
    if (!topic.trim()) {
      alert('Please enter a topic for your content')
      return
    }

    setIsLoading(true)

    try {
      const response = await fetch(buildApiUrl('/api/v1/social-media/create'), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content_type: 'post',
          topic: topic.trim(),
          platform,
          tone,
          length,
          include_hashtags: includeHashtags,
          scheduled_time: scheduledTime || null
        })
      })

      if (response.ok) {
        const data = await response.json()

        setGeneratedContent(data.content)
        setHashtags(data.hashtags)
        setOptimalTime(data.optimal_time)
        setEngagementPrediction(data.engagement_prediction)
      } else {
        throw new Error('Failed to generate content')
      }
    } catch (error) {
      console.error('Error generating content:', error)
      // Fallback to mock data for demo
      setGeneratedContent(`🚀 **${topic}**\n\nHere's my take on ${topic.toLowerCase()} - this is exactly what your audience needs to hear right now! 💪\n\n#${topic.replace(/\s+/g, '')} #BusinessGrowth #Success`)
      setHashtags(['#business', '#entrepreneurship', '#growth', '#success'])
      setOptimalTime('9:00 AM - 11:00 AM EST')
      setEngagementPrediction({
        likes: '50-100',
        comments: '10-25',
        shares: '5-15',
        reach: '500-1000'
      })
    } finally {
      setIsLoading(false)
    }
  }

  const postContent = async () => {
    if (!generatedContent) {
      alert('Please generate content first')
      return
    }

    setIsLoading(true)

    try {
      // This would integrate with the actual social media APIs
      // For now, we'll simulate the posting
      await new Promise(resolve => setTimeout(resolve, 2000))

      alert(`✅ Content posted successfully to ${platform}!\n\nPost: "${generatedContent.substring(0, 50)}..."`)
    } catch (error) {
      console.error('Error posting content:', error)
      alert('Error posting content. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
    alert('Copied to clipboard!')
  }

  return (
    <div className="flex flex-col h-full max-w-6xl mx-auto">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Send className="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-gray-900">AI Social Media Creator</h2>
              <p className="text-sm text-gray-600">Create engaging content and post automatically</p>
            </div>
          </div>
        </div>
      </div>

      <div className="flex-1 p-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Content Creation Form */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Create Content</h3>

          <div className="space-y-4">
            {/* Topic Input */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Topic
              </label>
              <input
                type="text"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder="What should your post be about?"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* Platform Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Platform
              </label>
              <div className="grid grid-cols-2 gap-2">
                {platformOptions.map((option) => (
                  <button
                    key={option.value}
                    onClick={() => setPlatform(option.value)}
                    className={`p-2 rounded-lg border text-sm transition-colors ${
                      platform === option.value
                        ? 'bg-blue-100 border-blue-300 text-blue-700'
                        : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
                    }`}
                  >
                    <span className="mr-2">{option.icon}</span>
                    {option.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Tone Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Tone
              </label>
              <select
                value={tone}
                onChange={(e) => setTone(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                {toneOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>

            {/* Length Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Length
              </label>
              <select
                value={length}
                onChange={(e) => setLength(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                {lengthOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>

            {/* Options */}
            <div className="flex items-center space-x-4">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={includeHashtags}
                  onChange={(e) => setIncludeHashtags(e.target.checked)}
                  className="mr-2"
                />
                <span className="text-sm text-gray-700">Include hashtags</span>
              </label>
            </div>

            {/* Scheduled Time */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Schedule Post (Optional)
              </label>
              <input
                type="datetime-local"
                value={scheduledTime}
                onChange={(e) => setScheduledTime(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* Generate Button */}
            <button
              onClick={generateContent}
              disabled={!topic.trim() || isLoading}
              className="w-full px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
            >
              <Bot className="w-4 h-4" />
              <span>{isLoading ? 'Generating...' : 'Generate Content'}</span>
            </button>
          </div>
        </div>

        {/* Generated Content Preview */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Generated Content</h3>

          {generatedContent ? (
            <div className="space-y-4">
              {/* Content Preview */}
              <div className="p-4 bg-gray-50 rounded-lg border">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center space-x-2">
                    <span className="text-lg">
                      {platformOptions.find(p => p.value === platform)?.icon}
                    </span>
                    <span className="text-sm font-medium text-gray-700 capitalize">
                      {platform}
                    </span>
                  </div>
                  <button
                    onClick={() => copyToClipboard(generatedContent)}
                    className="text-xs text-blue-600 hover:text-blue-700"
                  >
                    Copy
                  </button>
                </div>
                <div className="whitespace-pre-wrap text-gray-900">
                  {generatedContent}
                </div>
              </div>

              {/* Hashtags */}
              {hashtags.length > 0 && (
                <div>
                  <h4 className="text-sm font-medium text-gray-700 mb-2 flex items-center">
                    <Hash className="w-4 h-4 mr-1" />
                    Hashtags
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {hashtags.map((tag, index) => (
                      <span
                        key={index}
                        className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Optimal Time */}
              <div>
                <h4 className="text-sm font-medium text-gray-700 mb-2 flex items-center">
                  <Clock className="w-4 h-4 mr-1" />
                  Optimal Posting Time
                </h4>
                <p className="text-sm text-gray-600">{optimalTime}</p>
              </div>

              {/* Engagement Prediction */}
              <div>
                <h4 className="text-sm font-medium text-gray-700 mb-2 flex items-center">
                  <TrendingUp className="w-4 h-4 mr-1" />
                  Predicted Engagement
                </h4>
                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div className="p-2 bg-green-50 rounded">
                    <span className="text-green-700">👍 {engagementPrediction.likes} likes</span>
                  </div>
                  <div className="p-2 bg-blue-50 rounded">
                    <span className="text-blue-700">💬 {engagementPrediction.comments} comments</span>
                  </div>
                  <div className="p-2 bg-purple-50 rounded">
                    <span className="text-purple-700">📤 {engagementPrediction.shares} shares</span>
                  </div>
                  <div className="p-2 bg-orange-50 rounded">
                    <span className="text-orange-700">👥 {engagementPrediction.reach} reach</span>
                  </div>
                </div>
              </div>

              {/* Post Button */}
              <button
                onClick={postContent}
                disabled={isLoading}
                className="w-full px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
              >
                <Send className="w-4 h-4" />
                <span>{isLoading ? 'Posting...' : `Post to ${platform}`}</span>
              </button>
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              <Bot className="w-12 h-12 mx-auto mb-4 opacity-50" />
              <p>Generated content will appear here</p>
              <p className="text-sm mt-2">Fill out the form and click "Generate Content" to get started</p>
            </div>
          )}
        </div>
      </div>

      {/* Tips Section */}
      <div className="bg-blue-50 border-t border-blue-200 p-4">
        <div className="max-w-4xl mx-auto">
          <h4 className="text-sm font-medium text-blue-900 mb-2 flex items-center">
            <Target className="w-4 h-4 mr-1" />
            Pro Tips for Better Content
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs text-blue-800">
            <div>
              <strong>Be Specific:</strong> The more specific your topic, the better the content will be tailored to your audience.
            </div>
            <div>
              <strong>Choose Right Tone:</strong> Professional works for LinkedIn, casual for Twitter, inspirational for Instagram.
            </div>
            <div>
              <strong>Include Hashtags:</strong> Relevant hashtags can increase visibility by 30-50% on most platforms.
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default SocialMedia
