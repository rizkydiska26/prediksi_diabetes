"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { ArrowLeft, Sparkles, HelpCircle, Plus, Minus, Search, MessageSquare } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"

export default function FAQPage() {
  const [isVisible, setIsVisible] = useState(false)
  const [openFaq, setOpenFaq] = useState<number | null>(null)
  const [searchTerm, setSearchTerm] = useState("")

  useEffect(() => {
    setIsVisible(true)
  }, [])

  // Data FAQ
  const faqs = [
    {
      question: "Apa itu DiabCare?",
      answer:
        "DiabCare adalah website prediksi risiko diabetes yang dikembangkan oleh mahasiswa Sains Data Terapan PENS. Website ini membantu Anda menilai risiko diabetes berdasarkan beberapa parameter kesehatan seperti usia, kadar glukosa, insulin, dan BMI.",
      category: "umum",
    },
    {
      question: "Bagaimana cara menggunakan DiabCare?",
      answer:
        "Cukup masukkan data kesehatan Anda seperti usia, kadar glukosa, insulin, dan BMI pada halaman Prediksi. Sistem akan menganalisis data tersebut dan memberikan penilaian risiko diabetes Anda.",
      category: "penggunaan",
    },
    {
      question: "Apakah hasil prediksi DiabCare akurat?",
      answer:
        "DiabCare menggunakan model machine learning yang dilatih dengan dataset diabetes. Meskipun demikian, hasil prediksi hanya bersifat indikatif dan tidak menggantikan diagnosis medis profesional. Selalu konsultasikan dengan dokter untuk diagnosis yang tepat.",
      category: "akurasi",
    },
    {
      question: "Bagaimana cara mengetahui kadar glukosa saya?",
      answer:
        "Kadar glukosa dapat diukur melalui tes darah yang dilakukan di fasilitas kesehatan seperti rumah sakit, klinik, atau laboratorium. Anda juga dapat menggunakan alat pengukur glukosa darah (glukometer) di rumah.",
      category: "kesehatan",
    },
    {
      question: "Apa itu BMI dan bagaimana cara menghitungnya?",
      answer:
        "BMI (Body Mass Index) atau Indeks Massa Tubuh adalah ukuran yang digunakan untuk menilai apakah berat badan seseorang proporsional dengan tinggi badannya. BMI dihitung dengan membagi berat badan (dalam kilogram) dengan kuadrat tinggi badan (dalam meter). Rumusnya: BMI = Berat Badan (kg) / (Tinggi Badan (m) × Tinggi Badan (m)).",
      category: "kesehatan",
    },
    {
      question: "Apakah DiabCare dapat digunakan oleh semua orang?",
      answer:
        "DiabCare dapat digunakan oleh siapa saja yang ingin mengetahui risiko diabetes mereka, namun website ini dirancang khusus untuk orang dewasa dan tidak diperuntukkan bagi anak-anak atau remaja.",
      category: "penggunaan",
    },
    {
      question: "Bagaimana cara mencegah diabetes?",
      answer:
        "Beberapa cara untuk mencegah diabetes meliputi: menjaga berat badan ideal, melakukan aktivitas fisik secara teratur, mengonsumsi makanan sehat dan seimbang, mengurangi konsumsi gula dan karbohidrat olahan, serta menghindari merokok dan konsumsi alkohol berlebihan.",
      category: "kesehatan",
    },
    {
      question: "Apakah DiabCare tersedia dalam bahasa lain?",
      answer:
        "Saat ini, DiabCare hanya tersedia dalam Bahasa Indonesia. Kami berencana untuk menambahkan dukungan bahasa lain di masa mendatang.",
      category: "penggunaan",
    },
  ]

  // Filter FAQs based on search term
  const filteredFaqs = faqs.filter(
    (faq) =>
      faq.question.toLowerCase().includes(searchTerm.toLowerCase()) ||
      faq.answer.toLowerCase().includes(searchTerm.toLowerCase()),
  )

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
                className="font-medium transition-all duration-300 hover:text-green-200 hover:scale-105 relative group text-green-100"
              >
                Fitur
                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-green-200 transition-all duration-300 group-hover:w-full"></span>
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
                className="font-medium transition-all duration-300 hover:text-green-200 hover:scale-105 relative group text-white"
              >
                FAQ
                <span className="absolute -bottom-1 left-0 w-full h-0.5 bg-green-200 transition-all duration-300"></span>
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
          className={`text-center mb-12 transition-all duration-1000 ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"}`}
        >
          <Badge className="bg-gradient-to-r from-green-100 to-blue-100 text-green-800 mb-4 px-4 py-2 rounded-full">
            <HelpCircle className="w-4 h-4 mr-2 inline" />
            FAQ
          </Badge>
          <h1 className="text-3xl md:text-4xl font-bold mb-4">
            Pertanyaan yang{" "}
            <span className="bg-gradient-to-r from-green-600 to-blue-600 bg-clip-text text-transparent">
              Sering Diajukan
            </span>
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Temukan jawaban untuk pertanyaan umum tentang DiabCare dan diabetes.
          </p>
        </div>

        {/* Search Bar */}
        <div
          className={`max-w-3xl mx-auto mb-10 transition-all duration-1000 delay-300 ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"}`}
        >
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
            <Input
              type="text"
              placeholder="Cari pertanyaan..."
              className="pl-10 py-6 rounded-xl border-gray-200 focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all duration-300 shadow-md hover:shadow-lg"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        </div>

        <div
          className={`max-w-3xl mx-auto transition-all duration-1000 delay-500 ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"}`}
        >
          {filteredFaqs.length === 0 ? (
            <div className="text-center py-10">
              <HelpCircle className="h-16 w-16 mx-auto text-gray-300 mb-4" />
              <h3 className="text-xl font-medium text-gray-700 mb-2">Tidak ada hasil yang ditemukan</h3>
              <p className="text-gray-500">Coba kata kunci lain atau hubungi kami untuk pertanyaan lebih lanjut.</p>
            </div>
          ) : (
            filteredFaqs.map((faq, index) => (
              <div
                key={index}
                className={`mb-6 bg-white rounded-2xl shadow-md overflow-hidden transition-all duration-500 ${
                  openFaq === index ? "shadow-lg ring-2 ring-green-200" : "hover:shadow-lg"
                }`}
              >
                <div
                  className={`p-6 cursor-pointer transition-colors duration-300 ${
                    openFaq === index ? "bg-gradient-to-r from-green-50 to-blue-50" : "bg-white"
                  }`}
                  onClick={() => setOpenFaq(openFaq === index ? null : index)}
                >
                  <div className="flex justify-between items-center">
                    <h3
                      className={`text-lg font-medium ${
                        openFaq === index ? "text-green-700" : "text-gray-800"
                      } transition-colors duration-300 group-hover:text-green-700`}
                    >
                      {faq.question}
                    </h3>
                    <div
                      className={`p-2 rounded-full ${
                        openFaq === index ? "bg-green-100 text-green-600" : "bg-gray-100 text-gray-500"
                      } transition-colors duration-300`}
                    >
                      {openFaq === index ? <Minus className="h-4 w-4" /> : <Plus className="h-4 w-4" />}
                    </div>
                  </div>
                </div>

                {openFaq === index && (
                  <div className="p-6 bg-white border-t border-gray-100 animate-fadeIn">
                    <p className="text-gray-600 leading-relaxed">{faq.answer}</p>
                    <div className="mt-4 flex justify-end">
                      <Badge
                        className={`bg-opacity-20 text-xs ${
                          faq.category === "umum"
                            ? "bg-blue-100 text-blue-700"
                            : faq.category === "penggunaan"
                              ? "bg-green-100 text-green-700"
                              : faq.category === "akurasi"
                                ? "bg-purple-100 text-purple-700"
                                : faq.category === "kesehatan"
                                  ? "bg-amber-100 text-amber-700"
                                  : "bg-gray-100 text-gray-700"
                        }`}
                      >
                        {faq.category}
                      </Badge>
                    </div>
                  </div>
                )}
              </div>
            ))
          )}
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
                  <MessageSquare className="w-4 h-4 mr-2" />
                  Masih Punya Pertanyaan?
                </div>
                <h3 className="text-2xl md:text-3xl font-bold mb-4 leading-tight">
                  Hubungi Kami untuk Informasi Lebih Lanjut
                </h3>
                <p className="text-green-100 text-lg leading-relaxed">
                  Jika Anda memiliki pertanyaan lain yang tidak tercantum di sini, jangan ragu untuk menghubungi kami.
                </p>
              </div>
              <Dialog>
                <DialogTrigger asChild>
                  <Button className="bg-white text-green-600 hover:bg-green-50 text-lg py-6 px-8 rounded-2xl shadow-2xl transition-all duration-300 hover:scale-105 transform font-medium">
                    Hubungi Kami
                  </Button>
                </DialogTrigger>
                <DialogContent className="sm:max-w-md rounded-2xl">
                  <DialogHeader>
                    <DialogTitle className="text-xl font-bold text-center mb-4">Kontak Kami</DialogTitle>
                  </DialogHeader>
                  <div className="space-y-6 py-4">
                    <div className="flex items-center p-4 bg-gradient-to-r from-green-50 to-green-100 rounded-lg hover:shadow-md transition-all duration-300 group">
                      <div className="bg-green-100 p-3 rounded-full mr-4 group-hover:scale-110 transition-transform duration-300">
                        <span className="text-2xl">📱</span>
                      </div>
                      <div>
                        <h4 className="font-medium text-gray-900">WhatsApp</h4>
                        <a
                          href="https://wa.me/085806940713?text=Halo%20DiabCare,%20saya%20ingin%20bertanya%20tentang%20aplikasi%20prediksi%20diabetes."
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-green-600 hover:underline"
                        >
                          085806940713
                        </a>
                      </div>
                    </div>

                    <div className="flex items-center p-4 bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg hover:shadow-md transition-all duration-300 group">
                      <div className="bg-blue-100 p-3 rounded-full mr-4 group-hover:scale-110 transition-transform duration-300">
                        <span className="text-2xl">📧</span>
                      </div>
                      <div>
                        <h4 className="font-medium text-gray-900">Email</h4>
                        <a href="mailto:diabcare@gmail.com" className="text-blue-600 hover:underline">
                          diabcare@gmail.com
                        </a>
                      </div>
                    </div>

                    <div className="flex items-center p-4 bg-gradient-to-r from-purple-50 to-purple-100 rounded-lg hover:shadow-md transition-all duration-300 group">
                      <div className="bg-purple-100 p-3 rounded-full mr-4 group-hover:scale-110 transition-transform duration-300">
                        <span className="text-2xl">📍</span>
                      </div>
                      <div>
                        <h4 className="font-medium text-gray-900">Alamat</h4>
                        <p className="text-gray-600">PENS, Surabaya, Indonesia</p>
                      </div>
                    </div>
                  </div>
                </DialogContent>
              </Dialog>
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
