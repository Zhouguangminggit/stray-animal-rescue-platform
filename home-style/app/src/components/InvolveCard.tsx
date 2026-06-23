'use client'

import { motion } from 'framer-motion'

interface InvolveCardProps {
  title: string
  description: string
  cta: string
  image: string
  delay?: number
}

export default function InvolveCard({
  title,
  description,
  cta,
  image,
  delay = 0,
}: InvolveCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-50px' }}
      transition={{ duration: 0.5, delay, ease: 'easeOut' }}
      className="relative h-[400px] rounded-2xl overflow-hidden group cursor-pointer"
    >
      <div
        className="absolute inset-0 bg-cover bg-center transition-transform duration-500 group-hover:scale-105"
        style={{ backgroundImage: `url(${image})` }}
      />
      <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/30 to-transparent" />
      <div className="absolute inset-0 flex flex-col justify-end p-8">
        <h3 className="font-display text-2xl text-white mb-2">{title}</h3>
        <p className="text-white/80 text-sm mb-4">{description}</p>
        <span className="text-primary-light text-sm font-medium group-hover:underline transition-all duration-200 inline-flex items-center gap-1">
          {cta}
          <svg
            className="w-4 h-4 transition-transform duration-200 group-hover:translate-x-1"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 5l7 7-7 7"
            />
          </svg>
        </span>
      </div>
    </motion.div>
  )
}
