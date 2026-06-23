'use client'

import AnimatedSection from '@/components/AnimatedSection'
import InvolveCard from '@/components/InvolveCard'

const involvements = [
  {
    title: '领养一只宠物',
    description: '给流浪动物一个永远的家',
    cta: '查看待领养动物',
    image: '/images/adopt-family.jpg',
  },
  {
    title: '捐赠支持',
    description: '你的每一份捐赠都能拯救一个生命',
    cta: '立即捐赠',
    image: '/images/donate-support.jpg',
  },
  {
    title: '成为志愿者',
    description: '用你的时间和爱心帮助更多动物',
    cta: '申请志愿者',
    image: '/images/volunteer-work.jpg',
  },
]

export default function GetInvolvedSection() {
  return (
    <section id="involve" className="py-20 md:py-28 lg:py-32 bg-white">
      <div className="max-w-7xl mx-auto px-5 md:px-10 lg:px-20">
        {/* Header */}
        <div className="text-center mb-12 md:mb-16">
          <AnimatedSection>
            <span className="inline-block font-label text-lg md:text-xl text-primary bg-light-orange px-4 py-1.5 rounded-full -rotate-2 mb-4">
              加入行动
            </span>
          </AnimatedSection>
          <AnimatedSection delay={0.1}>
            <h2 className="font-display text-3xl md:text-4xl lg:text-5xl text-gradient">
              你可以怎样帮忙
            </h2>
          </AnimatedSection>
        </div>

        {/* Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {involvements.map((item, index) => (
            <InvolveCard
              key={index}
              title={item.title}
              description={item.description}
              cta={item.cta}
              image={item.image}
              delay={index * 0.15}
            />
          ))}
        </div>
      </div>
    </section>
  )
}
