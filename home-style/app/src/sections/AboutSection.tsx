'use client'

import AnimatedSection from '@/components/AnimatedSection'
import StarDecoration from '@/components/StarDecoration'
import CountUp from '@/components/CountUp'
import { ArrowRight } from 'lucide-react'

const stats = [
  { value: 3000, suffix: '+', label: '已救助动物' },
  { value: 80, suffix: '%', label: '成功领养率' },
  { value: 200, suffix: '+', label: '志愿者' },
]

export default function AboutSection() {
  return (
    <section id="about" className="py-20 md:py-28 lg:py-32 bg-warm-white">
      <div className="max-w-7xl mx-auto px-5 md:px-10 lg:px-20">
        <div className="flex flex-col lg:flex-row items-center gap-12 lg:gap-20">
          {/* Text Content */}
          <div className="lg:w-[55%]">
            <AnimatedSection direction="left">
              <span className="inline-block font-label text-lg md:text-xl text-primary bg-light-orange px-4 py-1.5 rounded-full -rotate-2 mb-4">
                关于我们
              </span>
            </AnimatedSection>

            <AnimatedSection direction="left" delay={0.1}>
              <h2 className="font-display text-3xl md:text-4xl lg:text-5xl text-gradient leading-tight mb-6">
                每一只流浪动物
                <br />
                都值得被温柔以待
              </h2>
            </AnimatedSection>

            <AnimatedSection direction="left" delay={0.2}>
              <div className="space-y-4 text-dark-text/80 leading-relaxed mb-8">
                <p>
                  流浪动物救助平台成立于 2015 年，是一个非营利性的动物保护组织。我们相信每一个生命都值得尊重和关爱，无论是流浪在街头的小猫，还是被遗弃的小狗。
                </p>
                <p>
                  多年来，我们已经救助了超过 3,000 只流浪动物，为它们提供医疗救助、食物、庇护，并成功帮助 80% 的救助动物找到了永远的家。
                </p>
              </div>
            </AnimatedSection>

            {/* Stats */}
            <AnimatedSection direction="left" delay={0.3}>
              <div className="flex flex-wrap gap-8 mb-8">
                {stats.map((stat, index) => (
                  <div key={index} className="text-center">
                    <div className="font-display text-3xl md:text-4xl text-gradient">
                      <CountUp
                        target={stat.value}
                        suffix={stat.suffix}
                      />
                    </div>
                    <p className="text-sm text-gray-text mt-1">{stat.label}</p>
                  </div>
                ))}
              </div>
            </AnimatedSection>

            <AnimatedSection direction="left" delay={0.4}>
              <button
                onClick={() => {
                  const el = document.querySelector('#services')
                  el?.scrollIntoView({ behavior: 'smooth' })
                }}
                className="inline-flex items-center gap-2 text-primary font-medium hover:underline underline-offset-4 transition-all duration-200"
              >
                了解更多
                <ArrowRight className="w-4 h-4" />
              </button>
            </AnimatedSection>
          </div>

          {/* Image */}
          <div className="lg:w-[45%] relative">
            <AnimatedSection direction="right" delay={0.2}>
              <div className="relative mx-auto lg:mx-0" style={{ maxWidth: '450px' }}>
                {/* Star Decorations */}
                <StarDecoration
                  className="absolute -top-4 -left-4 z-10"
                  size={40}
                  delay={0.5}
                />
                <StarDecoration
                  className="absolute top-1/4 -right-6 z-10"
                  size={32}
                  delay={0.7}
                />
                <StarDecoration
                  className="absolute -bottom-2 left-1/4 z-10"
                  size={36}
                  delay={0.9}
                />

                {/* Main Image */}
                <div className="relative aspect-square rounded-full overflow-hidden border-4 border-primary shadow-xl">
                  <img
                    src="/images/about-volunteer.jpg"
                    alt="志愿者与救助动物"
                    className="w-full h-full object-cover"
                  />
                </div>
              </div>
            </AnimatedSection>
          </div>
        </div>
      </div>
    </section>
  )
}
