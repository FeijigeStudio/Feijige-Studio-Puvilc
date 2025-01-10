'use client'

import { useState, useEffect } from 'react'
import { io } from 'socket.io-client'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"

// Initialize socket connection
const socket = io()

export default function ChatInterface() {
  const [currentUser, setCurrentUser] = useState<any>(null)
  const [currentChat, setCurrentChat] = useState<string | null>(null)
  const [message, setMessage] = useState('')
  const [messages, setMessages] = useState<any[]>([])
  const [friends, setFriends] = useState<any[]>([])
  const [friendUID, setFriendUID] = useState('')
  const [showAddFriend, setShowAddFriend] = useState(false)

  useEffect(() => {
    // Simulating user login (replace with actual login system)
    const username = prompt("Enter your username:")
    if (username) {
      socket.emit('login', username)
    }

    socket.on('login_response', (data) => {
      setCurrentUser(data.user)
      setFriends(data.friends)
    })

    socket.on('update_chat_list', (updatedFriends) => {
      setFriends(updatedFriends)
    })

    socket.on('chat_message', (data) => {
      if (data.chat === currentChat) {
        addMessage(data.sender, data.message)
      }
    })

    socket.on('add_friend_response', (response) => {
      if (response.success) {
        alert('Friend added successfully!')
        setFriends(response.friends)
      } else {
        alert('Failed to add friend: ' + response.message)
      }
      setShowAddFriend(false)
    })

    return () => {
      socket.off('login_response')
      socket.off('update_chat_list')
      socket.off('chat_message')
      socket.off('add_friend_response')
    }
  }, [currentChat])

  const addMessage = (sender: string, text: string) => {
    setMessages(prev => [...prev, { sender, text }])
  }

  const sendMessage = () => {
    if (message.trim() && currentChat) {
      socket.emit('send_message', { recipient: currentChat, message: message.trim() })
      addMessage(currentUser.username, message.trim())
      setMessage('')
    }
  }

  const handleAddFriend = () => {
    if (friendUID.trim()) {
      socket.emit('add_friend', { uid: friendUID.trim() })
      setFriendUID('')
    }
  }

  return (
    <Card className="w-[150px] h-[15vh] fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 flex flex-col overflow-hidden rounded-xl shadow-lg">
      <div className="bg-primary text-primary-foreground p-2 text-xs font-medium">
        Welcome, {currentUser?.username}
        <Dialog open={showAddFriend} onOpenChange={setShowAddFriend}>
          <DialogTrigger asChild>
            <Button 
              variant="secondary" 
              size="sm" 
              className="w-full mt-1 text-xs bg-green-500 hover:bg-green-600"
            >
              Add Friend
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-[200px]">
            <DialogHeader>
              <DialogTitle>Add Friend</DialogTitle>
            </DialogHeader>
            <div className="flex flex-col gap-2">
              <Input
                placeholder="Enter friend's UID"
                value={friendUID}
                onChange={(e) => setFriendUID(e.target.value)}
                className="text-xs"
              />
              <Button 
                onClick={handleAddFriend}
                className="text-xs"
              >
                Add
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      <div className="flex-1 overflow-y-auto p-2 bg-muted/50">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex ${msg.sender === currentUser?.username ? 'justify-end' : 'justify-start'} mb-1`}
          >
            <div
              className={`rounded-lg px-2 py-1 text-xs max-w-[80%] ${
                msg.sender === currentUser?.username
                  ? 'bg-primary text-primary-foreground'
                  : 'bg-background'
              }`}
            >
              {msg.text}
            </div>
          </div>
        ))}
      </div>

      <div className="p-2 flex gap-1 border-t">
        <Input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Type a message..."
          className="text-xs"
        />
        <Button 
          onClick={sendMessage}
          size="sm"
          className="text-xs"
        >
          Send
        </Button>
      </div>
    </Card>
  )
}

