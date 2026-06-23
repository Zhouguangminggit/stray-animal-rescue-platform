'use client'

import { Heart } from 'lucide-react'

const quickLinks = [
  { label: '关于我们', href: '#about' },
  { label: '领养动物', href: '#pets' },
  { label: '参与救助', href: '#involve' },
  { label: '新闻动态', href: '#' },
  { label: '隐私政策', href: '#' },
]

const socialLinks = [
  { label: '微信公众号', href: '#' },
  { label: '微博', href: '#' },
  { label: '抖音', href: '#' },
  { label: '小红书', href: '#' },
]

export default function Footer() {
  const scrollToSection = (href: string) => {
    if (href === '#') return
    const element = document.querySelector(href)
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' })
    }
  }

  return (
    <footer className="bg-dark-text text-white">
      <div className="max-w-7xl mx-auto px-5 md:px-10 lg:px-20 py-16 md:py-20">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10 lg:gap-8">
          {/* Brand */}
          <div>
            <h3 className="font-display text-2xl text-primary mb-4">
              Street Pet Society
            </h3>
            <p className="text-white/60 text-sm leading-relaxed">
              致力于救助流浪动物，为每一个生命带来希望和温暖。我们相信，爱能改变一切。
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-display text-lg mb-4">快速链接</h4>
            <ul className="space-y-3">
              {quickLinks.map((link, index) => (
                <li key={index}>
                  <button
                    onClick={() => scrollToSection(link.href)}
                    className="text-white/60 hover:text-primary text-sm transition-colors duration-200"
                  >
                    {link.label}
                  </button>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="font-display text-lg mb-4">联系方式</h4>
            <ul className="space-y-3 text-sm text-white/60">
              <li>北京市朝阳区爱心路 88 号</li>
              <li>+86 10-8888-9999</li>
              <li>contact@streetpetsociety.org</li>
            </ul>
          </div>

          {/* Social */}
          <div>
            <h4 className="font-display text-lg mb-4">关注我们</h4>
            <ul className="space-y-3">
              {socialLinks.map((link, index) => (
                <li key={index}>
                  <a
                    href={link.href}
                    className="text-white/60 hover:text-primary text-sm transition-colors duration-200 inline-flex items-center gap-2"
                  >
                    {link.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* Copyright */}
      <div className="border-t border-white/10">
        <div className="max-w-7xl mx-auto px-5 md:px-10 lg:px-20 py-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4 text-sm text-white/40">
            <p className="flex items-center gap-1">
              © 2025 Street Pet Society. 保留所有权利。
              <Heart className="w-3 h-3 text-primary fill-primary" />
            </p>
            <p>非营利组织 京ICP备XXXXXXXX号</p>
          </div>
        </div>
      </div>
    </footer>
  )
}
