'use client'

import { useEffect, useState } from 'react'
import { useSearchParams } from 'next/navigation'
import Link from 'next/link'
import { useTranslation } from 'next-i18next'
import { SearchBar } from '@/components/SearchBar'
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"

interface SearchResult {
  id: string
  title: string
  description: string
}

export default function SearchResults() {
  const [results, setResults] = useState<SearchResult[]>([])
  const searchParams = useSearchParams()
  const query = searchParams.get('q')
  const { t } = useTranslation()

  useEffect(() => {
    const fetchResults = async () => {
      // In a real application, this would be an API call to your backend
      // For demonstration, we're using mock data
      const mockResults: SearchResult[] = [
        { id: '1', title: 'Python Data Analysis', description: 'A project showcasing data analysis using Python' },
        { id: '2', title: 'React Component Library', description: 'A collection of reusable React components' },
        { id: '3', title: 'Machine Learning Model', description: 'An implementation of a machine learning algorithm' },
      ]
      setResults(mockResults)
    }

    if (query) {
      fetchResults()
    }
  }, [query])

  return (
    <div className="container mx-auto px-4 py-8">
      <SearchBar />
      <h1 className="text-3xl font-bold mt-8 mb-4">{t('searchResults')}: {query}</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {results.map((result) => (
          <Link href={`/code-showcase/${result.id}`} key={result.id}>
            <Card className="h-full hover:shadow-lg transition-shadow duration-200">
              <CardHeader>
                <CardTitle>{result.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <p>{result.description}</p>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  )
}

