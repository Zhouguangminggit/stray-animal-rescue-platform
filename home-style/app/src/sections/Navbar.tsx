'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Menu, Heart } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet'

const navLinks = [
  { label: '关于我们', href: '#about' },
  { label: '领养动物', href: '#pets' },
  { label: '参与救助', href: '#involve' },
  { label: '联系方式', href: '#contact' },
]

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false)
  const [mobileOpen, setMobileOpen] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 100)
    }
    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const scrollToSection = (href: string) => {
    const element = document.querySelector(href)
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' })
    }
    setMobileOpen(false)
  }

  return (
    <motion.header
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5, ease: 'easeOut' }}
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled
          ? 'bg-warm-white/95 backdrop-blur-xl shadow-nav'
          : 'bg-transparent'
      }`}
    >
      <nav className="max-w-7xl mx-auto px-5 md:px-10 lg:px-20 h-[72px] flex items-center justify-between">
        {/* Logo */}
        <a
          href="#"
          onClick={(e) => {
            e.preventDefault()
            window.scrollTo({ top: 0, behavior: 'smooth' })
          }}
          className="font-display text-xl md:text-2xl text-primary transition-colors duration-200"
        >
          Street Pet Society
        </a>

        {/* Desktop Nav Links */}
        <div className="hidden md:flex items-center gap-8">
          {navLinks.map((link) => (
            <button
              key={link.href}
              onClick={() => scrollToSection(link.href)}
              className={`text-sm font-medium transition-colors duration-200 hover:text-primary ${
                scrolled ? 'text-dark-text' : 'text-white'
              }`}
            >
              {link.label}
            </button>
          ))}
        </div>

        {/* Desktop CTA */}
        <div className="hidden md:block">
          <Button
            onClick={() => scrollToSection('#involve')}
            className="bg-gradient-primary hover:opacity-90 text-white rounded-full px-6 py-2 text-sm font-medium transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lg"
          >
            <Heart className="w-4 h-4 mr-2" />
            立即捐赠
          </Button>
        </div>

        {/* Mobile Menu */}
        <Sheet open={mobileOpen} onOpenChange={setMobileOpen}>
          <SheetTrigger asChild className="md:hidden">
            <button
              className={`p-2 rounded-lg transition-colors ${
                scrolled ? 'text-dark-text' : 'text-white'
              }`}
            >
              <Menu className="w-6 h-6" />
            </button>
          </SheetTrigger>
          <SheetContent side="right" className="bg-warm-white border-border-orange w-[300px]">
            <div className="flex flex-col gap-6 mt-8">
              {navLinks.map((link) => (
                <button
                  key={link.href}
                  onClick={() => scrollToSection(link.href)}
                  className="text-lg text-dark-text hover:text-primary transition-colors duration-200 text-left font-medium"
                >
                  {link.label}
                </button>
              ))}
              <Button
                onClick={() => scrollToSection('#involve')}
                className="bg-gradient-primary hover:opacity-90 text-white rounded-full px-6 py-3 text-sm font-medium mt-4"
              >
                <Heart className="w-4 h-4 mr-2" />
                立即捐赠
              </Button>
            </div>
          </SheetContent>
        </Sheet>
      </nav>
    </motion.header>
  )
}
