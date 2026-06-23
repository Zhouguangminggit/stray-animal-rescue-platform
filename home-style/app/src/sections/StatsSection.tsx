'use client'

import { motion } from 'framer-motion'
import CountUp from '@/components/CountUp'
import { PawPrint, Heart, Stethoscope, Users } from 'lucide-react'

const stats = [
  { icon: PawPrint, value: 3000, suffix: '+', label: '已救助动物' },
  { icon: Heart, value: 2500, suffix: '+', label: '成功领养' },
  { icon: Stethoscope, value: 15000, suffix: '+', label: '提供医疗服务' },
  { icon: Users, value: 500, suffix: '+', label: '活跃志愿者' },
]

export default function StatsSection() {
  return (
    <section className="py-16 md:py-20 lg:py-24 bg-gradient-stats">
      <div className="max-w-7xl mx-auto px-5 md:px-10 lg:px-20">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-8 lg:gap-12">
          {stats.map((stat, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-50px' }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="text-center"
            >
              <div className="inline-flex items-center justify-center w-14 h-14 rounded-full bg-white/20 mb-4">
                <stat.icon className="w-7 h-7 text-white" />
              </div>
              <div className="font-display text-3xl md:text-4xl lg:text-5xl text-white mb-2">
                <CountUp target={stat.value} suffix={stat.suffix} />
              </div>
              <p className="text-white/80 text-sm md:text-base">{stat.label}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
