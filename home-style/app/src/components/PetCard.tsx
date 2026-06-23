'use client'

import { motion } from 'framer-motion'

interface PetCardProps {
  name: string
  age: string
  breed: string
  description: string
  image: string
  delay?: number
}

export default function PetCard({
  name,
  age,
  breed,
  description,
  image,
  delay = 0,
}: PetCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-50px' }}
      transition={{ duration: 0.5, delay, ease: 'easeOut' }}
      className="flex-shrink-0 w-[280px] bg-white rounded-2xl overflow-hidden shadow-card hover:shadow-card-hover transition-all duration-300 group"
    >
      <div className="relative w-full h-[280px] overflow-hidden">
        <img
          src={image}
          alt={name}
          className="w-full h-full object-cover transition-transform duration-400 group-hover:scale-105"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end justify-center pb-4">
          <span className="text-white text-sm font-medium px-4 py-2 bg-primary/90 rounded-full">
            了解更多
          </span>
        </div>
      </div>
      <div className="p-5">
        <div className="flex items-center justify-between mb-2">
          <h3 className="font-display text-lg text-dark-text">{name}</h3>
          <span className="text-xs text-primary bg-light-orange px-2 py-1 rounded-full">
            {age}
          </span>
        </div>
        <p className="text-xs text-gray-text mb-2">{breed}</p>
        <p className="text-sm text-dark-text/70">{description}</p>
      </div>
    </motion.div>
  )
}
