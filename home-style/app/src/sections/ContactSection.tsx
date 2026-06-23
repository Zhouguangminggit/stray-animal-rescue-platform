'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import AnimatedSection from '@/components/AnimatedSection'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { MapPin, Phone, Mail, Clock, CheckCircle } from 'lucide-react'

const contactInfo = [
  {
    icon: MapPin,
    label: '地址',
    value: '北京市朝阳区爱心路 88 号',
  },
  {
    icon: Phone,
    label: '电话',
    value: '+86 10-8888-9999',
  },
  {
    icon: Mail,
    label: '邮箱',
    value: 'contact@streetpetsociety.org',
  },
  {
    icon: Clock,
    label: '工作时间',
    value: '周一至周六 9:00-18:00',
  },
]

export default function ContactSection() {
  const [submitted, setSubmitted] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    subject: '',
    message: '',
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitted(true)
    setTimeout(() => {
      setSubmitted(false)
      setFormData({ name: '', email: '', phone: '', subject: '', message: '' })
    }, 3000)
  }

  return (
    <section id="contact" className="py-20 md:py-28 lg:py-32 bg-warm-white">
      <div className="max-w-7xl mx-auto px-5 md:px-10 lg:px-20">
        <div className="flex flex-col lg:flex-row gap-12 lg:gap-20">
          {/* Contact Info */}
          <div className="lg:w-[45%]">
            <AnimatedSection direction="left">
              <span className="inline-block font-label text-lg md:text-xl text-primary bg-light-orange px-4 py-1.5 rounded-full -rotate-2 mb-4">
                联系我们
              </span>
            </AnimatedSection>

            <AnimatedSection direction="left" delay={0.1}>
              <h2 className="font-display text-3xl md:text-4xl lg:text-5xl text-dark-text leading-tight mb-6">
                一起为流浪动物
                <br />
                创造更美好的未来
              </h2>
            </AnimatedSection>

            <AnimatedSection direction="left" delay={0.2}>
              <p className="text-gray-text leading-relaxed mb-8">
                无论您是想领养宠物、捐赠支持，还是申请成为志愿者，我们都期待与您联系。每一份力量都能帮助更多流浪动物找到温暖的家。
              </p>
            </AnimatedSection>

            <div className="space-y-5">
              {contactInfo.map((item, index) => (
                <AnimatedSection key={index} direction="left" delay={0.3 + index * 0.1}>
                  <div className="flex items-start gap-4">
                    <div className="w-11 h-11 rounded-xl bg-light-orange flex items-center justify-center flex-shrink-0">
                      <item.icon className="w-5 h-5 text-primary" />
                    </div>
                    <div>
                      <p className="text-sm text-gray-text mb-0.5">{item.label}</p>
                      <p className="text-dark-text font-medium">{item.value}</p>
                    </div>
                  </div>
                </AnimatedSection>
              ))}
            </div>
          </div>

          {/* Contact Form */}
          <div className="lg:w-[55%]">
            <AnimatedSection direction="right" delay={0.2}>
              <form
                onSubmit={handleSubmit}
                className="bg-white rounded-2xl p-6 md:p-8 shadow-card"
              >
                {submitted ? (
                  <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="flex flex-col items-center justify-center py-12"
                  >
                    <CheckCircle className="w-16 h-16 text-green-500 mb-4" />
                    <h3 className="font-display text-2xl text-dark-text mb-2">
                      消息已发送
                    </h3>
                    <p className="text-gray-text text-center">
                      感谢您的留言，我们会尽快与您联系！
                    </p>
                  </motion.div>
                ) : (
                  <>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                      <div>
                        <Label htmlFor="name" className="text-dark-text mb-2 block">
                          姓名 <span className="text-red-500">*</span>
                        </Label>
                        <Input
                          id="name"
                          required
                          value={formData.name}
                          onChange={(e) =>
                            setFormData({ ...formData, name: e.target.value })
                          }
                          className="bg-warm-white border-border-orange focus:border-primary focus:ring-primary/20 h-12"
                          placeholder="请输入您的姓名"
                        />
                      </div>
                      <div>
                        <Label htmlFor="email" className="text-dark-text mb-2 block">
                          邮箱 <span className="text-red-500">*</span>
                        </Label>
                        <Input
                          id="email"
                          type="email"
                          required
                          value={formData.email}
                          onChange={(e) =>
                            setFormData({ ...formData, email: e.target.value })
                          }
                          className="bg-warm-white border-border-orange focus:border-primary focus:ring-primary/20 h-12"
                          placeholder="请输入您的邮箱"
                        />
                      </div>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                      <div>
                        <Label htmlFor="phone" className="text-dark-text mb-2 block">
                          电话
                        </Label>
                        <Input
                          id="phone"
                          type="tel"
                          value={formData.phone}
                          onChange={(e) =>
                            setFormData({ ...formData, phone: e.target.value })
                          }
                          className="bg-warm-white border-border-orange focus:border-primary focus:ring-primary/20 h-12"
                          placeholder="请输入您的电话（选填）"
                        />
                      </div>
                      <div>
                        <Label htmlFor="subject" className="text-dark-text mb-2 block">
                          主题
                        </Label>
                        <Select
                          value={formData.subject}
                          onValueChange={(value) =>
                            setFormData({ ...formData, subject: value })
                          }
                        >
                          <SelectTrigger className="bg-warm-white border-border-orange focus:border-primary focus:ring-primary/20 h-12">
                            <SelectValue placeholder="请选择主题" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="adopt">领养咨询</SelectItem>
                            <SelectItem value="donate">捐赠咨询</SelectItem>
                            <SelectItem value="volunteer">志愿者申请</SelectItem>
                            <SelectItem value="other">其他</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                    </div>

                    <div className="mb-6">
                      <Label htmlFor="message" className="text-dark-text mb-2 block">
                        留言内容 <span className="text-red-500">*</span>
                      </Label>
                      <Textarea
                        id="message"
                        required
                        value={formData.message}
                        onChange={(e) =>
                          setFormData({ ...formData, message: e.target.value })
                        }
                        className="bg-warm-white border-border-orange focus:border-primary focus:ring-primary/20 min-h-[120px] resize-none"
                        placeholder="请输入您想告诉我们的内容..."
                      />
                    </div>

                    <Button
                      type="submit"
                      className="w-full bg-gradient-primary hover:opacity-90 text-white rounded-full py-6 text-base font-medium transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lg"
                    >
                      发送消息
                    </Button>
                  </>
                )}
              </form>
            </AnimatedSection>
          </div>
        </div>
      </div>
    </section>
  )
}
