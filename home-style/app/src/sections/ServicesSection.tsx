'use client'

import AnimatedSection from '@/components/AnimatedSection'
import ServiceCard from '@/components/ServiceCard'
import {
  PawPrint,
  HeartPulse,
  Home,
  BookOpen,
  Users,
  ShieldPlus,
} from 'lucide-react'

const services = [
  {
    icon: PawPrint,
    title: '动物救助',
    description:
      '我们在城市各个角落寻找需要帮助的流浪动物，为受伤、生病或饥饿的动物提供及时的救援。',
  },
  {
    icon: HeartPulse,
    title: '医疗救助',
    description:
      '提供疫苗接种、绝育手术、伤病治疗等全面的医疗服务，确保每只动物都健康快乐地生活。',
  },
  {
    icon: Home,
    title: '领养服务',
    description:
      '为每只动物寻找最合适的 forever home，严格的领养审核确保动物和新家庭都能获得幸福。',
  },
  {
    icon: BookOpen,
    title: '社区教育',
    description:
      '通过学校讲座、社区活动等方式，宣传动物保护理念，培养下一代对生命的尊重和关爱。',
  },
  {
    icon: Users,
    title: '志愿者招募',
    description:
      '欢迎热爱动物的志愿者加入我们的大家庭，无论是照顾动物、参与活动还是协助办公。',
  },
  {
    icon: ShieldPlus,
    title: '绝育计划',
    description:
      '推行 TNR（捕捉-绝育-放归）计划，从根本上控制流浪动物数量，减少更多生命的流浪。',
  },
]

export default function ServicesSection() {
  return (
    <section id="services" className="py-20 md:py-28 lg:py-32 bg-white">
      <div className="max-w-7xl mx-auto px-5 md:px-10 lg:px-20">
        {/* Header */}
        <div className="text-center mb-12 md:mb-16">
          <AnimatedSection>
            <span className="inline-block font-label text-lg md:text-xl text-primary bg-light-orange px-4 py-1.5 rounded-full -rotate-2 mb-4">
              我们的服务
            </span>
          </AnimatedSection>
          <AnimatedSection delay={0.1}>
            <h2 className="font-display text-3xl md:text-4xl lg:text-5xl text-gradient">
              我们能做什么
            </h2>
          </AnimatedSection>
        </div>

        {/* Services Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {services.map((service, index) => (
            <ServiceCard
              key={index}
              icon={service.icon}
              title={service.title}
              description={service.description}
              delay={index * 0.1}
            />
          ))}
        </div>
      </div>
    </section>
  )
}
