'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { ChatHeader } from './chat-header'
import { ChatMessages } from './chat-messages'
import { ChatInput } from './chat-input'
import { Button } from '@/components/ui/button'
import { useToast } from '@/components/ui/use-toast'
import { cn } from '@/lib/utils'

export default function ChatPage() {
  const [messages, setMessages] = useState<{ text: string; sender: 'user' | 'bot' }[]>([])
  const [language, setLanguage] = useState<'en' | 'zh'>('en')
  const router = useRouter()
  const { toast } = useToast()

  const translations = {
    en: {
      title: 'Chat - Feijige Studio',
      switchLanguage: 'Switch to 中文',
      inputPlaceholder: 'Type your message...',
      send: 'Send',
    },
    zh: {
      title: '聊天 - 飞鸡阁工作室',
      switchLanguage: 'Switch to English',
      inputPlaceholder: '输入您的消息...',
      send: '发送',
    },
  }

  useEffect(() => {
    document.title = translations[language].title
  }, [language])

  const switchLanguage = () => {
    setLanguage(prev => (prev === 'en' ? 'zh
