'use client'

import { useRouter } from 'next/navigation'
import { usePathname } from 'next/navigation'
import { Button } from "@/components/ui/button"
import { useTranslation } from 'next-i18next'

export default function LanguageSwitcher() {
  const router = useRouter()
  const pathname = usePathname()
  const { i18n } = useTranslation()

  const switchLanguage = (lang: string) => {
    i18n.changeLanguage(lang)
    router.push(pathname, undefined, { locale: lang })
  }

  return (
    <div className="fixed top-4 right-4 flex space-x-2 bg-white rounded-full shadow-md p-1 z-50">
      <Button 
        variant="ghost" 
        size="sm" 
        onClick={() => switchLanguage('en')}
        className={`font-semibold ${i18n.language === 'en' ? 'bg-primary text-primary-foreground' : ''}`}
      >
        EN
      </Button>
      <Button 
        variant="ghost" 
        size="sm" 
        onClick={() => switchLanguage('zh')}
        className={`font-semibold ${i18n.language === 'zh' ? 'bg-primary text-primary-foreground' : ''}`}
      >
        中文
      </Button>
    </div>
  )
}

