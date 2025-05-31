"use client"

import { useEffect, useState } from "react"
import { motion, useScroll, useTransform } from "framer-motion"
import { ArrowRight } from "lucide-react"
import { Button } from "@/components/ui/button"
import Link from "next/link"

export function ParallaxHero() {
  const [isMounted, setIsMounted] = useState(false)
  const { scrollY } = useScroll()

  // Parallax effects
  const y1 = useTransform(scrollY, [0, 500], [0, -150])
  const y2 = useTransform(scrollY, [0, 500], [0, -100])
  const y3 = useTransform(scrollY, [0, 500], [0, -50])
  const opacity = useTransform(scrollY, [0, 300], [1, 0])

  useEffect(() => {
    setIsMounted(true)
  }, [])

  if (!isMounted) {
    return null
  }

  return (
    <div className="relative h-screen overflow-hidden bg-gradient-to-b from-green-50 to-white">
      {/* Background elements */}
      <motion.div style={{ y: y1, opacity }} className="absolute inset-0 z-0">
        <div className="absolute top-20 left-20 w-64 h-64 bg-green-200 rounded-full opacity-30 blur-3xl" />
        <div className="absolute bottom-40 right-20 w-80 h-80 bg-blue-200 rounded-full opacity-30 blur-3xl" />
      </motion.div>

      {/* Content */}
      <div className="container mx-auto px-4 h-full flex flex-col justify-center relative z-10">
        <div className="max-w-3xl">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
            <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold mb-6">
              Kenali Risiko <span className="text-green-600">Diabetes</span> Anda Sekarang
            </h1>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <p className="text-xl text-gray-600 mb-8 max-w-2xl">
              DiabCare membantu Anda memahami dan mengelola faktor risiko diabetes dengan mudah. Dapatkan penilaian
              risiko diabetes berdasarkan metrik kesehatan Anda.
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="flex flex-col sm:flex-row gap-4"
          >
            <Link href="/prediksi" passHref>
              <Button className="bg-green-600 hover:bg-green-700 text-white text-lg py-6 px-8 rounded-xl shadow-lg hover:shadow-xl transition-all">
                Mulai Prediksi <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
            <Link href="/fitur" passHref>
              <Button
                variant="outline"
                className="border-green-600 text-green-600 hover:bg-green-50 text-lg py-6 px-8 rounded-xl"
              >
                Pelajari Lebih Lanjut
              </Button>
            </Link>
          </motion.div>
        </div>
      </div>

      {/* Foreground elements */}
      <motion.div
        style={{ y: y3 }}
        className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-white to-transparent z-20"
      />
    </div>
  )
}
