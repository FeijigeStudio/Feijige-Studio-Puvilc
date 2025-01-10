import LanguageSwitcher from './components/LanguageSwitcher'

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-100">
      <LanguageSwitcher />
      <main className="container mx-auto px-4 py-16">
        <h1 className="text-4xl font-bold text-center mb-8">Feijige Studio</h1>
        {/* Add other content here */}
      </main>
    </div>
  )
}

