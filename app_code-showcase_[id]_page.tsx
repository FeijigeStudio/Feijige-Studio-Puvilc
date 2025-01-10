'use client'

import { useParams } from 'next/navigation'
import { useTranslation } from 'next-i18next'
import { LanguageSwitcher } from '@/components/LanguageSwitcher'

export default function CodeShowcase() {
  const { id } = useParams()
  const { t } = useTranslation()

  // In a real application, you would fetch the project details based on the id
  const project = {
    title: 'Sample Project',
    description: 'This is a sample project description.',
    code: `function helloWorld() {
  console.log("Hello, Feijige Studio!");
}

helloWorld();`
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <LanguageSwitcher />
      <main className="container mx-auto px-4 py-16">
        <h1 className="text-3xl font-bold mb-4">{project.title}</h1>
        <p className="mb-8">{project.description}</p>
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">{t('code')}</h2>
          <pre className="bg-gray-100 p-4 rounded overflow-x-auto">
            <code>{project.code}</code>
          </pre>
        </div>
      </main>
    </div>
  )
}

