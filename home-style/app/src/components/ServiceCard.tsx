'use client'

import { motion } from 'framer-motion'
import type { LucideIcon } from 'lucide-react'

interface ServiceCardProps {
  icon: LucideIcon
  title: string
  description: string
  delay?: number
}

export default function ServiceCard({
  icon: Icon,
  title,
  description,
  delay = 0,
}: ServiceCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-50px' }}
      transition={{ duration: 0.5, delay, ease: 'easeOut' }}
      whileHover={{ y: -4 }}
      className="bg-white rounded-2xl p-8 shadow-card hover:shadow-card-hover transition-shadow duration-300"
    >
      <div className="w-14 h-14 rounded-xl bg-light-orange flex items-center justify-center mb-5 group-hover:bg-primary transition-colors duration-300">
        <Icon className="w-7 h-7 text-primary" />
      </div>
      <h3 className="font-display text-xl text-dark-text mb-3">{title}</h3>
      <p className="text-gray-text text-sm leading-relaxed">{description}</p>
    </motion.div>
  )
}
