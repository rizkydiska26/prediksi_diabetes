"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { ArrowLeft, ArrowRight, Activity, Heart, Droplet, Scale, Apple, AlertCircle, Sparkles, Zap } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"

export default function FiturPage() {
  const [isVisible, setIsVisible] = useState(false)
  const [activeFeature, setActiveFeature] = useState<number | null>(null)

  useEffect(() => {
    setIsVisible(true)
  }, [])

  const features = [
    {
      icon: <Activity className="h-10 w-10" />,
      title: "Deteksi Dini",
      description: "Identifikasi risiko diabetes sejak dini dengan prediksi berbasis machine learning yang akurat.",
      color: "from-green-500 to-green-600",
      bgColor: "from-green-50 to-green-100",
    },
    {
      icon: <Heart className="h-10 w-10" />,
      title: "Pemantauan Kesehatan",
      description: "Pantau faktor kesehatan utama yang mempengaruhi risiko diabetes Anda.",
      color: "from-blue-500 to-blue-600",
      bgColor: "from-blue-50 to-blue-100",
    },
    {
      icon: <AlertCircle className="h-10 w-10" />,
      title: "Penilaian Risiko",
      description: "Dapatkan penilaian risiko diabetes berdasarkan data kesehatan Anda secara real-time.",
      color: "from-purple-500 to-purple-600",
      bgColor: "from-purple-50 to-purple-100",
    },
    {
      icon: <Droplet className="h-10 w-10" />,
      title: "Analisis Glukosa",
      description: "Pahami bagaimana kadar glukosa memengaruhi risiko diabetes Anda.",
      color: "from-cyan-500 to-cyan-600",
      bgColor: "from-cyan-50 to-cyan-100",
    },
    {
      icon: <Scale className="h-10 w-10" />,
      title: "Evaluasi BMI",
      description: "Ketahui bagaimana BMI Anda berkontribusi terhadap risiko diabetes.",
      color: "from-amber-500 to-amber-600",
      bgColor: "from-amber-50 to-amber-100",
    },
    {
      icon: <Apple className="h-10 w-10" />,
      title: "Rekomendasi Makanan Sehat",
      description:
        "Dapatkan rekomendasi makanan sehat yang sesuai untuk penderita diabetes guna membantu menjaga kadar gula darah agar tetap stabil.",
      color: "from-emerald-500 to-emerald-600",
      bgColor: "from-emerald-50 to-emerald-100",
    },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-blue-50 to-purple-50 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-green-200 to-green-300 rounded-full opacity-20 animate-pulse"></div>
        <div
          className="absolute top-1/2 -left-20 w-60 h-60 bg-gradient-to-br from-blue-200 to-blue-300 rounded-full opacity-20 animate-bounce"
          style={{ animationDuration: "3s" }}
        ></div>
        <div
          className="absolute bottom-20 right-1/4 w-40 h-40 bg-gradient-to-br from-purple-200 to-purple-300 rounded-full opacity-20 animate-ping"
          style={{ animationDuration: "4s" }}
        ></div>
      </div>

      {/* Header */}
      <header className="bg-gradient-to-r from-green-600 via-green-700 to-green-800 text-white py-4 sticky top-0 z-50 shadow-xl">
        <div className="container mx-auto px-4">
          <div className="flex justify-between items-center">
            {/* Logo */}
            <Link href="/" className="flex items-center group">
              <div className="relative">
                <img
                  src="/logo.png"
                  alt="DiabCare Logo"
                  className="h-12 w-auto transition-transform duration-300 group-hover:scale-110"
                />
                <div className="absolute -inset-1 bg-white rounded-full opacity-0 group-hover:opacity-20 transition-opacity duration-300"></div>
              </div>
              <span className="ml-2 font-bold text-xl bg-gradient-to-r from-white to-green-100 bg-clip-text text-transparent">
                DiabCare
              </span>
            </Link>

            {/* Menu Desktop */}
            <nav className="hidden md:flex items-center space-x-8">
              <Link
                href="/"
                className="font-medium transition-all duration-300 hover:text-green-200 hover:scale-105 relative group text-green-100"
              >
                Beranda
                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-green-200 transition-all duration-300 group-hover:w-full"></span>
              </Link>
              <Link
                href="/fitur"
                className="font-medium transition-all duration-300 hover:text-green-200 hover:scale-105 relative group text-white"
              >
                Fitur
                <span className="absolute -bottom-1 left-0 w-full h-0.5 bg-green-200 transition-all duration-300"></span>
              </Link>
              <Link
                href="/statistik"
                className="font-medium transition-all duration-300 hover:text-green-200 hover:scale-105 relative group text-green-100"
              >
                Statistik
                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-green-200 transition-all duration-300 group-hover:w-full"></span>
              </Link>
              <Link
                href="/testimonial"
                className="font-medium transition-all duration-300 hover:text-green-200 hover:scale-105 relative group text-green-100"
              >
                Testimonial
                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-green-200 transition-all duration-300 group-hover:w-full"></span>
              </Link>
              <Link
                href="/faq"
                className="font-medium transition-all duration-300 hover:text-green-200 hover:scale-105 relative group text-green-100"
              >
                FAQ
                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-green-200 transition-all duration-300 group-hover:w-full"></span>
              </Link>
              <Link href="/prediksi" passHref>
                <Button className="bg-white text-green-600 hover:bg-green-100 px-6 py-3 rounded-full font-medium transition-all duration-300 hover:scale-105 hover:shadow-lg">
                  <span className="flex items-center">
                    <Sparkles className="w-4 h-4 mr-2" />
                    Mulai Prediksi
                  </span>
                </Button>
              </Link>
            </nav>

            {/* Menu Mobile - Simplified */}
            <div className="md:hidden">
              <Link href="/prediksi" passHref>
                <Button className="bg-white text-green-600 hover:bg-green-100 px-4 py-2 rounded-full font-medium transition-all duration-300 hover:scale-105">
                  Mulai Prediksi
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8 relative z-10">
        <Link
          href="/"
          className="inline-flex items-center text-green-600 hover:text-green-700 mb-8 group transition-all duration-300"
        >
          <ArrowLeft className="mr-2 h-5 w-5 transition-transform duration-300 group-hover:-translate-x-1" />
          <span>Kembali ke Beranda</span>
        </Link>

        <div
          className={`text-center mb-16 transition-all duration-1000 ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"}`}
        >
          <Badge className="bg-gradient-to-r from-green-100 to-blue-100 text-green-800 mb-4 px-4 py-2 rounded-full">
            <Zap className="w-4 h-4 mr-2 inline" />
            Fitur Utama
          </Badge>
          <h1 className="text-3xl md:text-4xl font-bold mb-4">
            Kenapa Menggunakan{" "}
            <span className="bg-gradient-to-r from-green-600 to-blue-600 bg-clip-text text-transparent">DiabCare</span>?
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            DiabCare menawarkan berbagai fitur untuk membantu Anda memahami dan mengelola risiko diabetes dengan lebih
            baik.
          </p>
        </div>

        <div
          className={`grid md:grid-cols-3 gap-8 transition-all duration-1000 delay-300 ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"}`}
        >
          {features.map((feature, index) => (
            <div
              key={index}
              className={`group bg-white p-6 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-500 hover:scale-105 transform cursor-pointer border border-gray-100 bg-gradient-to-br ${feature.bgColor} hover:bg-white`}
              onMouseEnter={() => setActiveFeature(index)}
              onMouseLeave={() => setActiveFeature(null)}
            >
              <div
                className={`w-16 h-16 rounded-2xl bg-gradient-to-r ${feature.color} flex items-center justify-center mb-6 group-hover:scale-110 group-hover:rotate-3 transition-all duration-300 shadow-lg`}
              >
                <div className="text-white">{feature.icon}</div>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3 group-hover:text-gray-800 transition-colors duration-300">
                {feature.title}
              </h3>
              <p className="text-gray-600 group-hover:text-gray-700 transition-colors duration-300 leading-relaxed">
                {feature.description}
              </p>
              <div
                className={`mt-4 flex justify-end transition-opacity duration-300 ${activeFeature === index ? "opacity-100" : "opacity-0"}`}
              >
                <div className={`p-2 rounded-full bg-gradient-to-r ${feature.color} text-white`}>
                  <ArrowRight className="h-4 w-4" />
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-16 relative">
          <div className="absolute inset-0 bg-gradient-to-r from-green-200 to-blue-200 rounded-3xl blur-xl opacity-30"></div>
          <div className="relative bg-gradient-to-r from-green-600 via-green-700 to-blue-600 rounded-3xl p-8 md:p-12 text-white shadow-2xl overflow-hidden">
            {/* Animated background elements */}
            <div className="absolute top-0 right-0 w-64 h-64 bg-white opacity-10 rounded-full -translate-y-1/2 translate-x-1/2 animate-pulse"></div>
            <div
              className="absolute bottom-0 left-0 w-48 h-48 bg-white opacity-10 rounded-full translate-y-1/2 -translate-x-1/2 animate-bounce"
              style={{ animationDuration: "3s" }}
            ></div>
            <div
              className="absolute top-1/2 left-1/2 w-32 h-32 bg-white opacity-5 rounded-full -translate-x-1/2 -translate-y-1/2 animate-spin"
              style={{ animationDuration: "10s" }}
            ></div>

            <div className="flex flex-col md:flex-row items-center justify-between relative z-10">
              <div className="mb-6 md:mb-0 md:w-2/3">
                <div className="inline-flex items-center px-4 py-2 bg-white bg-opacity-20 rounded-full text-white text-sm font-medium mb-4">
                  <Sparkles className="w-4 h-4 mr-2" />
                  Mulai Sekarang
                </div>
                <h3 className="text-2xl md:text-3xl font-bold mb-4 leading-tight">
                  Mulai Prediksi Diabetes Anda Sekarang
                </h3>
                <p className="text-green-100 text-lg leading-relaxed">
                  DiabCare dapat membantu Anda mengetahui risiko diabetes Anda dengan mudah melalui informasi kesehatan Anda.
                </p>
              </div>
              <Link
                href="/prediksi"
                className="group bg-white text-green-600 hover:bg-green-50 text-lg py-6 px-8 rounded-2xl shadow-2xl inline-flex items-center transition-all duration-300 hover:scale-105 transform font-medium"
              >
                <span className="flex items-center">
                  <Sparkles className="mr-2 h-5 w-5" />
                  Mulai Prediksi
                  <ArrowRight className="ml-2 h-5 w-5 transition-transform duration-300 group-hover:translate-x-1" />
                </span>
              </Link>
            </div>
          </div>
        </div>
      </main>

      {/* Enhanced Footer */}
      <footer className="bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900 text-white py-12 relative overflow-hidden mt-12">
        <div className="absolute inset-0 bg-gradient-to-r from-green-900 to-blue-900 opacity-10"></div>
        <div className="container mx-auto px-4 relative z-10">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div className="group">
              <div className="flex items-center mb-4">
                <img
                  src="/logo.png"
                  alt="DiabCare Logo"
                  className="h-10 w-auto mr-2 transition-transform duration-300 group-hover:scale-110"
                />
                <span className="font-bold text-xl bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
                  DiabCare
                </span>
              </div>
              <p className="text-gray-400 mb-4 leading-relaxed">
                Aplikasi prediksi risiko diabetes yang dikembangkan oleh mahasiswa Sains Data Terapan PENS.
              </p>
            </div>

            {[
              {
                title: "Navigasi",
                links: [
                  { href: "/", label: "Beranda" },
                  { href: "/fitur", label: "Fitur" },
                  { href: "/statistik", label: "Statistik" },
                  { href: "/testimonial", label: "Testimonial" },
                  { href: "/faq", label: "FAQ" },
                ],
              },
              {
                title: "Fitur",
                links: [
                  { href: "/prediksi", label: "Prediksi Diabetes" },
                  { href: "/fitur", label: "Pemantauan Kesehatan" },
                  { href: "/fitur", label: "Analisis Glukosa" },
                  { href: "/fitur", label: "Evaluasi BMI" },
                  { href: "/fitur", label: "Rekomendasi Makanan Sehat" },
                ],
              },
            ].map((section, index) => (
              <div key={index}>
                <h4 className="font-bold text-lg mb-4 text-white">{section.title}</h4>
                <ul className="space-y-2">
                  {section.links.map((link, linkIndex) => (
                    <li key={linkIndex}>
                      <Link
                        href={link.href}
                        className="text-gray-400 hover:text-white transition-all duration-300 hover:translate-x-1 inline-block"
                      >
                        {link.label}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            ))}

            <div>
              <h4 className="font-bold text-lg mb-4 text-white">Kontak</h4>
              <ul className="space-y-3">
                {[
                  { icon: "📧", text: "diabcare@gmail.com" },
                  { icon: "📱", text: "085806940713" },
                  { icon: "📍", text: "PENS, Surabaya, Indonesia" },
                ].map((contact, index) => (
                  <li
                    key={index}
                    className="flex items-center text-gray-400 hover:text-white transition-colors duration-300 group"
                  >
                    <span className="mr-3 text-lg group-hover:scale-110 transition-transform duration-300">
                      {contact.icon}
                    </span>
                    <span>{contact.text}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-700 pt-8 flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-400 mb-4 md:mb-0">© 2025 DiabCare - Aplikasi Prediksi Diabetes</p>
            <p className="text-gray-400">Dikembangkan oleh Mahasiswa Sains Data Terapan PENS</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
