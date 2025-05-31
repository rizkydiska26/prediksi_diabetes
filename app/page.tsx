"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { ArrowRight, Activity, Heart, AlertCircle, Sparkles, TrendingUp, Shield } from "lucide-react"

export default function Home() {
  const [isVisible, setIsVisible] = useState(false)
  const [currentStat, setCurrentStat] = useState(0)

  useEffect(() => {
    setIsVisible(true)

    // Animate stats counter
    const interval = setInterval(() => {
      setCurrentStat((prev) => (prev + 1) % 3)
    }, 3000)

    return () => clearInterval(interval)
  }, [])

  const stats = [
    {
      value: "589",
      label: "Juta",
      description: "Penderita diabetes di seluruh dunia",
      color: "from-green-400 to-green-600",
    },
    {
      value: "10.6%",
      label: "Populasi",
      description: "Populasi penderita diabetes di Indonesia",
      color: "from-blue-400 to-blue-600",
    },
    {
      value: "50%",
      label: "Kasus",
      description: "Tidak terdiagnosis dengan baik",
      color: "from-purple-400 to-purple-600",
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
      <header className="bg-gradient-to-r from-green-600 via-green-700 to-green-800 text-white py-4 sticky top-0 z-50 shadow-xl backdrop-blur-sm">
        <div className="container mx-auto px-4">
          <div className="flex justify-between items-center">
            {/* Logo with animation */}
            <div className="flex items-center group">
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
            </div>

            {/* Menu Desktop with hover effects */}
            <nav className="hidden md:flex items-center space-x-8">
              {[
                { href: "/", label: "Beranda", active: true },
                { href: "/fitur", label: "Fitur" },
                { href: "/statistik", label: "Statistik" },
                { href: "/testimonial", label: "Testimonial" },
                { href: "/faq", label: "FAQ" },
              ].map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`font-medium transition-all duration-300 hover:text-green-200 hover:scale-105 relative group ${
                    item.active ? "text-white" : "text-green-100"
                  }`}
                >
                  {item.label}
                  <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-green-200 transition-all duration-300 group-hover:w-full"></span>
                </Link>
              ))}
              <Link
                href="/prediksi"
                className="bg-white text-green-600 hover:bg-green-100 px-6 py-3 rounded-full font-medium transition-all duration-300 hover:scale-105 hover:shadow-lg transform"
              >
                <span className="flex items-center">
                  <Sparkles className="w-4 h-4 mr-2" />
                  Mulai Prediksi
                </span>
              </Link>
            </nav>

            {/* Mobile Menu */}
            <div className="md:hidden">
              <Link
                href="/prediksi"
                className="bg-white text-green-600 hover:bg-green-100 px-4 py-2 rounded-full font-medium transition-all duration-300 hover:scale-105"
              >
                Mulai Prediksi
              </Link>
            </div>
          </div>
        </div>
      </header>

      <main>
        {/* Hero Section with enhanced animations */}
        <div className="bg-gradient-to-br from-green-50 via-green-100 to-blue-100 relative">
          <div className="container mx-auto px-4">
            <div className="flex flex-col md:flex-row items-center min-h-[calc(100vh-76px)]">
              <div
                className={`md:w-1/2 py-10 md:py-0 transition-all duration-1000 ${isVisible ? "opacity-100 translate-x-0" : "opacity-0 -translate-x-10"}`}
              >
                <div className="space-y-6">
                  <div className="inline-flex items-center px-4 py-2 bg-green-100 rounded-full text-green-800 text-sm font-medium animate-bounce">
                    <TrendingUp className="w-4 h-4 mr-2" />
                    Platform Prediksi Diabetes Terdepan
                  </div>

                  <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-gray-900 mb-4 leading-tight">
                    Kenali Risiko{" "}
                    <span className="bg-gradient-to-r from-green-600 via-green-500 to-blue-500 bg-clip-text text-transparent animate-pulse">
                      Diabetes
                    </span>{" "}
                    Anda Sekarang
                  </h1>

                  <p className="text-lg md:text-xl text-gray-600 mb-8 max-w-xl leading-relaxed">
                    DiabCare membantu Anda memantau dan mengelola faktor risiko diabetes dengan cara yang mudah dan efektif. Dapatkan penilaian risiko diabetes yang akurat berdasarkan data kesehatan pribadi Anda.
                  </p>

                  <div className="flex flex-col sm:flex-row gap-4">
                    <Link
                      href="/prediksi"
                      className="group bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white text-lg py-6 px-8 rounded-xl inline-flex items-center justify-center transition-all duration-300 hover:scale-105 hover:shadow-2xl transform"
                    >
                      <span className="flex items-center">
                        Mulai Prediksi
                        <ArrowRight className="ml-2 h-5 w-5 transition-transform duration-300 group-hover:translate-x-1" />
                      </span>
                    </Link>
                    <Link
                      href="/fitur"
                      className="group border-2 border-green-600 text-green-600 hover:bg-green-600 hover:text-white text-lg py-6 px-8 rounded-xl inline-flex items-center justify-center transition-all duration-300 hover:scale-105 hover:shadow-lg"
                    >
                      <span className="flex items-center">
                        <Shield className="mr-2 h-5 w-5" />
                        Pelajari Lebih Lanjut
                      </span>
                    </Link>
                  </div>
                </div>
              </div>

              <div
                className={`md:w-1/2 md:pl-10 transition-all duration-1000 delay-300 ${isVisible ? "opacity-100 translate-x-0" : "opacity-0 translate-x-10"}`}
              >
                <div className="relative group">
                  <div className="absolute -inset-4 bg-gradient-to-r from-green-200 via-blue-200 to-purple-200 rounded-3xl blur-2xl opacity-30 group-hover:opacity-50 transition-opacity duration-500"></div>
                  <div className="absolute -inset-2 bg-gradient-to-r from-green-300 to-blue-300 rounded-2xl blur-xl opacity-20 animate-pulse"></div>
                  <img
                    src="/diabetes-care.png"
                    alt="DiabCare Consultation"
                    className="relative z-10 rounded-2xl shadow-2xl mx-auto w-full h-auto transition-transform duration-500 group-hover:scale-105"
                    style={{ maxHeight: "600px", objectFit: "contain" }}
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Enhanced Stats Section */}
        <section className="py-20 bg-white relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-r from-green-50 to-blue-50 opacity-50"></div>
          <div className="container mx-auto px-4 relative z-10">
            <div className="text-center mb-16">
              <div className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-green-100 to-blue-100 rounded-full text-green-800 text-sm font-medium mb-4">
                <TrendingUp className="w-4 h-4 mr-2" />
                Data Terkini
              </div>
              <h2 className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent mb-4">
                Diabetes dalam Angka
              </h2>
              <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                Diabetes adalah masalah kesehatan global yang memengaruhi jutaan orang Kenali faktanya sekarang 
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-8">
              {stats.map((stat, index) => (
                <div
                  key={index}
                  className={`group bg-white p-8 rounded-2xl shadow-lg hover:shadow-2xl text-center transition-all duration-500 hover:scale-105 transform cursor-pointer border border-gray-100 ${
                    currentStat === index ? "ring-2 ring-green-400 ring-opacity-50" : ""
                  }`}
                >
                  <div className="flex flex-col items-center">
                    <div
                      className={`w-16 h-16 rounded-full bg-gradient-to-r ${stat.color} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300`}
                    >
                      <Sparkles className="w-8 h-8 text-white" />
                    </div>
                    <span
                      className={`text-4xl md:text-5xl font-bold bg-gradient-to-r ${stat.color} bg-clip-text text-transparent mb-2 transition-all duration-300`}
                    >
                      {stat.value}
                    </span>
                    <span className="text-xl font-medium text-gray-700 mb-4">{stat.label}</span>
                    <p className="text-gray-600 group-hover:text-gray-700 transition-colors duration-300">
                      {stat.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Enhanced Features Preview */}
        <section className="py-20 bg-gradient-to-br from-gray-50 to-green-50 relative">
          <div className="container mx-auto px-4">
            <div className="text-center mb-16">
              <div className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-green-100 to-blue-100 rounded-full text-green-800 text-sm font-medium mb-4">
                <Shield className="w-4 h-4 mr-2" />
                Fitur Unggulan
              </div>
              <h2 className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent mb-4">
                Kenapa Menggunakan DiabCare?
              </h2>
              <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                DiabCare menawarkan berbagai fitur untuk membantu Anda memahami dan mengelola risiko diabetes dengan
                lebih baik.
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-8">
              {[
                {
                  icon: Activity,
                  title: "Deteksi Dini",
                  description:
                    "Identifikasi risiko diabetes sejak dini dengan prediksi berbasis machine learning yang akurat.",
                  color: "from-green-500 to-green-600",
                  bgColor: "from-green-50 to-green-100",
                },
                {
                  icon: Heart,
                  title: "Pemantauan Kesehatan",
                  description: "Pantau faktor kesehatan utama yang mempengaruhi risiko diabetes Anda.",
                  color: "from-blue-500 to-blue-600",
                  bgColor: "from-blue-50 to-blue-100",
                },
                {
                  icon: AlertCircle,
                  title: "Penilaian Risiko",
                  description: "Dapatkan penilaian risiko diabetes berdasarkan data kesehatan Anda secara real-time.",
                  color: "from-purple-500 to-purple-600",
                  bgColor: "from-purple-50 to-purple-100",
                },
              ].map((feature, index) => (
                <div
                  key={index}
                  className={`group bg-white p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-500 hover:scale-105 transform cursor-pointer border border-gray-100 bg-gradient-to-br ${feature.bgColor} hover:bg-white`}
                >
                  <div
                    className={`w-16 h-16 rounded-2xl bg-gradient-to-r ${feature.color} flex items-center justify-center mb-6 group-hover:scale-110 group-hover:rotate-3 transition-all duration-300 shadow-lg`}
                  >
                    <feature.icon className="h-8 w-8 text-white" />
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 mb-3 group-hover:text-gray-800 transition-colors duration-300">
                    {feature.title}
                  </h3>
                  <p className="text-gray-600 group-hover:text-gray-700 transition-colors duration-300 leading-relaxed">
                    {feature.description}
                  </p>
                </div>
              ))}
            </div>

            <div className="text-center mt-12">
              <Link
                href="/fitur"
                className="group inline-flex items-center px-8 py-4 bg-gradient-to-r from-green-600 to-blue-600 text-white rounded-xl hover:from-green-700 hover:to-blue-700 transition-all duration-300 hover:scale-105 hover:shadow-lg font-medium"
              >
                <span>Lihat Semua Fitur</span>
                <ArrowRight className="ml-2 h-5 w-5 transition-transform duration-300 group-hover:translate-x-1" />
              </Link>
            </div>
          </div>
        </section>

        {/* Enhanced CTA */}
        <section className="py-20 bg-white">
          <div className="container mx-auto px-4">
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
        </section>
      </main>

      {/* Enhanced Footer */}
      <footer className="bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900 text-white py-12 relative overflow-hidden">
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
