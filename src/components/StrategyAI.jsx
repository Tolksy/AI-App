import React, { useState, useEffect, useRef } from 'react'
import { Send, Bot, User, Lightbulb, Target, TrendingUp, Brain, MessageCircle } from 'lucide-react'

// Fallback strategy responses for production
const getFallbackStrategyResponse = (message) => {
  const lowerMessage = message.toLowerCase()
  
  if (lowerMessage.includes('automotive') || lowerMessage.includes('car') || lowerMessage.includes('vehicle')) {
    return `Excellent! The automotive industry has tremendous lead generation potential. Here's my strategy for automotive sales:

🎯 **Target Audience**: Car buyers, fleet managers, auto enthusiasts, service customers

📈 **Lead Generation Channels**:
• Google My Business optimization for local visibility
• Facebook/Instagram ads targeting car enthusiasts
• LinkedIn outreach to fleet managers
• Partner with auto service centers
• Trade-in lead magnets ("Get Your Car's Value")

💡 **Proven Tactics**:
• "Free Car Value Check" landing pages
• Video testimonials from satisfied customers
• Seasonal campaigns (summer road trips, winter prep)
• Referral programs with existing customers

Would you like me to create a detailed execution plan for any of these strategies?`
  }
  
  if (lowerMessage.includes('real estate') || lowerMessage.includes('property') || lowerMessage.includes('home')) {
    return `Perfect! Real estate is one of the most profitable niches for lead generation. Here's my proven strategy:

🏠 **Target Audience**: Home buyers, sellers, investors, renters

📊 **High-Converting Lead Magnets**:
• Free home value reports
• Neighborhood market analysis
• First-time buyer guides
• Investment property calculators

🎯 **Multi-Channel Approach**:
• Facebook/Instagram ads (high engagement)
• Google Ads for "homes for sale" keywords
• Zillow/Realtor.com lead generation
• Referral partnerships with mortgage brokers
• Content marketing (market updates, neighborhood guides)

💼 **Automation Tools**:
• CRM with automated follow-up sequences
• Email drip campaigns for different buyer stages
• SMS for urgent property alerts

Ready to dive deeper into any of these strategies?`
  }
  
  if (lowerMessage.includes('saas') || lowerMessage.includes('software') || lowerMessage.includes('tech')) {
    return `Awesome! SaaS lead generation is my specialty. Here's a battle-tested strategy:

🚀 **SaaS Lead Generation Framework**:
• Free trial/demo signups
• Content marketing (blogs, webinars, ebooks)
• Product Hunt launches
• LinkedIn outreach to decision makers
• Retargeting campaigns for trial users

🎯 **High-Value Lead Magnets**:
• Free tool/calculator related to your software
• Industry reports and whitepapers
• Free consultation calls
• ROI calculators

📈 **Conversion Optimization**:
• A/B test landing pages
• Personalized demo experiences
• Social proof and case studies
• Free trial with guided onboarding

What type of SaaS are you building? I can create a customized strategy based on your target market.`
  }
  
  if (lowerMessage.includes('healthcare') || lowerMessage.includes('medical') || lowerMessage.includes('doctor')) {
    return `Healthcare lead generation requires special expertise due to compliance requirements. Here's my proven approach:

🏥 **Healthcare-Specific Strategies**:
• Educational content (health tips, condition guides)
• Patient testimonials and success stories
• Local SEO for medical practices
• Community health events and sponsorships

📋 **Compliant Lead Magnets**:
• Free health screenings
• Wellness guides and checklists
• Appointment booking systems
• Health assessment tools

⚖️ **Compliance Considerations**:
• HIPAA-compliant lead capture forms
• Clear privacy policies
• Opt-in consent for all communications
• Secure data handling practices

What type of healthcare practice are you working with? I can tailor the strategy to your specific specialty.`
  }
  
  // Default response for other queries
  return `I'm your Lead Generation Strategy AI Expert! While the full backend isn't connected, I can still help you create winning strategies.

Here are my core expertise areas:

🎯 **Industries I Excel In**:
• Automotive & Transportation
• Real Estate & Property
• SaaS & Technology
• Healthcare & Medical
• E-commerce & Retail
• Professional Services

🚀 **Proven Strategies**:
• Multi-channel lead generation
• Conversion optimization
• Lead nurturing sequences
• Local business marketing
• B2B outreach campaigns
• Social media lead generation

💡 **What I Can Help With**:
• Creating industry-specific strategies
• Designing lead magnets
• Setting up conversion funnels
• Automating follow-up sequences
• Optimizing for your target audience

What industry are you in, or what specific challenge are you trying to solve? I'll create a customized strategy for you!`
}

const StrategyAI = () => {
  const [messages, setMessages] = useState([])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [conversationHistory, setConversationHistory] = useState([])
  const messagesEndRef = useRef(null)

  useEffect(() => {
    // Initialize with welcome message
    const welcomeMessage = {
      id: 'welcome',
      type: 'assistant',
      message: "Hi! I'm your Lead Generation Strategy AI Expert. I can help you create winning lead generation strategies for any business niche. What industry are you in, or what would you like to know about lead generation?",
      suggestions: [
        "I'm in automotive sales",
        "I run a real estate business", 
        "I have a SaaS company",
        "I'm in healthcare",
        "Help me find leads for this software",
        "Show me your expertise areas"
      ],
      timestamp: new Date().toISOString()
    }
    setMessages([welcomeMessage])
  }, [])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const sendMessage = async (message = inputMessage) => {
    if (!message.trim()) return

    const userMessage = {
      id: Date.now().toString(),
      type: 'user',
      message: message.trim(),
      timestamp: new Date().toISOString()
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsLoading(true)

    // Check if we're in production (no backend available)
    const isProduction = process.env.NODE_ENV === 'production' && !window.location.hostname.includes('localhost')
    
    if (isProduction) {
      // Use fallback response in production
      setTimeout(() => {
        const aiMessage = {
          id: (Date.now() + 1).toString(),
          type: 'assistant',
          message: getFallbackStrategyResponse(message.trim()),
          suggestions: [
            "Tell me more about your industry",
            "Create a lead generation strategy",
            "Show me your expertise areas",
            "Help me find leads for this software"
          ],
          timestamp: new Date().toISOString()
        }
        setMessages(prev => [...prev, aiMessage])
        setIsLoading(false)
      }, 1500)
      return
    }

    try {
      const response = await fetch('http://localhost:8000/api/v1/strategy/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message.trim(),
          context: {
            timestamp: new Date().toISOString(),
            user_id: 'current_user'
          }
        })
      })

      if (response.ok) {
        const data = await response.json()
        
        const aiMessage = {
          id: (Date.now() + 1).toString(),
          type: 'assistant',
          message: data.message,
          suggestions: data.suggestions || [],
          strategy: data.strategy,
          execution_plan: data.execution_plan,
          timestamp: new Date().toISOString()
        }

        setMessages(prev => [...prev, aiMessage])
      } else {
        throw new Error('Failed to get response')
      }
    } catch (error) {
      console.error('Error sending message:', error)
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        message: getFallbackStrategyResponse(message.trim()),
        suggestions: [
          "Tell me more about your industry",
          "Create a lead generation strategy",
          "Show me your expertise areas"
        ],
        timestamp: new Date().toISOString()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleSuggestionClick = (suggestion) => {
    setInputMessage(suggestion)
    sendMessage(suggestion)
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const clearConversation = async () => {
    const isProduction = process.env.NODE_ENV === 'production' && !window.location.hostname.includes('localhost')
    
    if (!isProduction) {
      try {
        await fetch('http://localhost:8000/api/v1/strategy/conversation/clear', {
          method: 'DELETE'
        })
      } catch (error) {
        console.error('Error clearing conversation:', error)
      }
    }
    
    setMessages([])
    // Re-add welcome message
    const welcomeMessage = {
      id: 'welcome',
      type: 'assistant',
      message: "Hi! I'm your Lead Generation Strategy AI Expert. I can help you create winning lead generation strategies for any business niche. What industry are you in, or what would you like to know about lead generation?",
      suggestions: [
        "I'm in automotive sales",
        "I run a real estate business", 
        "I have a SaaS company",
        "I'm in healthcare",
        "Help me find leads for this software",
        "Show me your expertise areas"
      ],
      timestamp: new Date().toISOString()
    }
    setMessages([welcomeMessage])
  }

  const getMessageIcon = (type) => {
    if (type === 'user') {
      return <User className="w-5 h-5" />
    }
    return <Bot className="w-5 h-5" />
  }

  const getMessageTypeIcon = (messageType) => {
    const icons = {
      'niche_expertise': <Target className="w-4 h-4" />,
      'strategy_created': <Lightbulb className="w-4 h-4" />,
      'plan_execution': <TrendingUp className="w-4 h-4" />,
      'self_referential': <Brain className="w-4 h-4" />,
      'general_advice': <MessageCircle className="w-4 h-4" />
    }
    return icons[messageType] || <MessageCircle className="w-4 h-4" />
  }

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Brain className="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-gray-900">Lead Generation Strategy AI</h2>
              <p className="text-sm text-gray-600">Expert in all business niches • Creates execution plans • Finds leads 24/7</p>
            </div>
          </div>
          <button
            onClick={clearConversation}
            className="text-sm text-gray-500 hover:text-gray-700"
          >
            Clear Chat
          </button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div key={message.id} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`flex max-w-3xl ${message.type === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
              {/* Avatar */}
              <div className={`flex-shrink-0 ${message.type === 'user' ? 'ml-3' : 'mr-3'}`}>
                <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                  message.type === 'user' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-100 text-gray-600'
                }`}>
                  {getMessageIcon(message.type)}
                </div>
              </div>

              {/* Message Content */}
              <div className={`flex-1 ${message.type === 'user' ? 'text-right' : 'text-left'}`}>
                <div className={`inline-block p-4 rounded-lg ${
                  message.type === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-white border border-gray-200'
                }`}>
                  {/* Message Type Indicator */}
                  {message.type === 'assistant' && message.type && (
                    <div className="flex items-center mb-2 text-xs text-gray-500">
                      {getMessageTypeIcon(message.type)}
                      <span className="ml-1 capitalize">{message.type.replace('_', ' ')}</span>
                    </div>
                  )}

                  {/* Message Text */}
                  <div className="whitespace-pre-wrap">{message.message}</div>

                  {/* Strategy/Execution Plan */}
                  {message.strategy && (
                    <div className="mt-3 p-3 bg-gray-50 rounded border">
                      <h4 className="font-semibold text-sm text-gray-900 mb-2">Strategy Created:</h4>
                      <pre className="text-xs text-gray-700 whitespace-pre-wrap">
                        {JSON.stringify(message.strategy, null, 2)}
                      </pre>
                    </div>
                  )}

                  {message.execution_plan && (
                    <div className="mt-3 p-3 bg-blue-50 rounded border">
                      <h4 className="font-semibold text-sm text-blue-900 mb-2">Execution Plan:</h4>
                      <pre className="text-xs text-blue-800 whitespace-pre-wrap">
                        {message.execution_plan}
                      </pre>
                    </div>
                  )}

                  {/* Suggestions */}
                  {message.suggestions && message.suggestions.length > 0 && (
                    <div className="mt-3">
                      <div className="flex flex-wrap gap-2">
                        {message.suggestions.map((suggestion, index) => (
                          <button
                            key={index}
                            onClick={() => handleSuggestionClick(suggestion)}
                            className="text-xs bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-1 rounded-full border"
                          >
                            {suggestion}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                {/* Timestamp */}
                <div className={`text-xs text-gray-500 mt-1 ${
                  message.type === 'user' ? 'text-right' : 'text-left'
                }`}>
                  {new Date(message.timestamp).toLocaleTimeString()}
                </div>
              </div>
            </div>
          </div>
        ))}

        {/* Loading Indicator */}
        {isLoading && (
          <div className="flex justify-start">
            <div className="flex max-w-3xl">
              <div className="flex-shrink-0 mr-3">
                <div className="w-8 h-8 rounded-full bg-gray-100 text-gray-600 flex items-center justify-center">
                  <Bot className="w-5 h-5" />
                </div>
              </div>
              <div className="flex-1">
                <div className="inline-block p-4 rounded-lg bg-white border border-gray-200">
                  <div className="flex items-center space-x-2">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                    <span className="text-sm text-gray-600">AI is thinking...</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="bg-white border-t border-gray-200 p-4">
        <div className="flex space-x-3">
          <div className="flex-1">
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me about lead generation strategy, your industry, or how to find leads..."
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              rows={2}
            />
          </div>
          <button
            onClick={() => sendMessage()}
            disabled={!inputMessage.trim() || isLoading}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
          >
            <Send className="w-4 h-4" />
            <span>Send</span>
          </button>
        </div>
        
        {/* Quick Actions */}
        <div className="mt-3 flex flex-wrap gap-2">
          <button
            onClick={() => handleSuggestionClick("Help me find leads for this software")}
            className="text-xs bg-blue-100 hover:bg-blue-200 text-blue-700 px-3 py-1 rounded-full border"
          >
            Find leads for this software
          </button>
          <button
            onClick={() => handleSuggestionClick("Show me your expertise areas")}
            className="text-xs bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-1 rounded-full border"
          >
            Show expertise areas
          </button>
          <button
            onClick={() => handleSuggestionClick("Create a strategy for my business")}
            className="text-xs bg-green-100 hover:bg-green-200 text-green-700 px-3 py-1 rounded-full border"
          >
            Create strategy
          </button>
        </div>
      </div>
    </div>
  )
}

export default StrategyAI



