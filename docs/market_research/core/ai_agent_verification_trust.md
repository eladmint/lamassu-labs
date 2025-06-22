# AI Agent Verification and Trust: Current Challenges and Market Barriers

## TL;DR

**Market Size**: AI agents market growing from $5.25B (2024) to $52.62B (2030) at 46.3% CAGR.

**Key Problems**:
- 74% of organizations struggle to achieve AI value due to verification challenges
- 96% of tech professionals see AI agents as growing risk
- Current verification methods (manual testing, vendor docs) inadequate for dynamic agents
- "Black box" problem prevents understanding of agent decision-making

**Major Pain Points**:
- No standardized metrics for agent performance
- IP protection concerns prevent proper verification
- Trust issues in marketplaces (HuggingFace security, OpenAI verification failures)
- $13B annual losses from AI failures and trust issues

**Opportunity**: Zero-knowledge proofs can enable verification without exposing proprietary algorithms or data, addressing the core trust barrier in AI agent adoption.

## Executive Summary

The AI agent marketplace is experiencing explosive growth, with the global AI agents market projected to expand from $5.25 billion in 2024 to $52.62 billion by 2030, representing a CAGR of 46.3%<sup>[1](#ref1)</sup>. However, enterprises face significant challenges in verifying AI agent capabilities, performance, and trustworthiness, creating substantial barriers to widespread adoption. Recent industry data reveals that 74% of organizations struggle to achieve and scale AI value<sup>[2](#ref2)</sup>, while 96% of technology professionals consider AI agents a growing risk<sup>[3](#ref3)</sup>. These verification challenges are hampering the potential of a technology that could contribute $19.9 trillion to the global economy by 2030<sup>[4](#ref4)</sup>.

## Current Methods of AI Agent Verification and Their Limitations

### Traditional Verification Approaches

Current AI agent verification methods rely heavily on manual processes and basic testing frameworks that prove inadequate for complex agentic systems<sup>[5](#ref5)</sup>. Enterprise verification approaches typically include:

**Static Testing Methods**: Organizations primarily use basic functional testing and performance benchmarks to evaluate AI agents<sup>[6](#ref6)</sup>. However, these methods fail to capture the dynamic nature of agentic AI systems that can self-modify and generate sub-agents<sup>[3](#ref3)</sup>.

**Vendor-Provided Documentation**: Most enterprises rely on vendor documentation and case studies to assess AI agent capabilities<sup>[7](#ref7)</sup>. Yet this approach lacks independent verification, with around half of respondents to the 2024 AI Survey reporting having only a "partial understanding" of the AI technologies they use<sup>[8](#ref8)</sup>.

**Human-in-the-Loop Validation**: Many organizations employ human oversight for AI agent outputs, with 27% of respondents whose organizations use generative AI reporting that employees review all content created by AI before use<sup>[6](#ref6)</sup>. However, this approach is resource-intensive and doesn't scale effectively for autonomous agents.

### Fundamental Limitations

The current verification landscape suffers from several critical shortcomings:

**Black Box Problem**: AI agents, particularly those based on large language models, suffer from opacity in decision-making processes<sup>[9](#ref9)</sup>. This "black box" problem makes it difficult for enterprises to understand how agents arrive at specific decisions, creating trust and accountability issues<sup>[9](#ref9)</sup>.

**Lack of Standardized Metrics**: The industry lacks universally accepted standards for measuring AI agent performance, reliability, and safety<sup>[10](#ref10)</sup>. This absence of standardization makes it difficult to compare agents across different vendors and use cases<sup>[11](#ref11)</sup>.

**Dynamic Behavior Challenges**: Unlike traditional software, AI agents can exhibit non-deterministic behavior and adapt their responses based on new data<sup>[12](#ref12)</sup><sup>[13](#ref13)</sup>. Current verification methods struggle to account for this dynamic nature, particularly when agents operate autonomously without human oversight<sup>[3](#ref3)</sup>.

## Trust Issues in AI Agent Marketplaces

### HuggingFace Security Concerns

HuggingFace, hosting over 1 million AI models, has become a significant target for cybersecurity threats<sup>[14](#ref14)</sup>. The platform faces challenges with malicious actors uploading compromised models, with security experts noting that "the sheer scale of the problem makes it challenging" to address comprehensively<sup>[14](#ref14)</sup>. While HuggingFace has integrated commercial scanning tools and started verifying profiles of major tech companies, security measures are "significantly trailing behind the explosive growth of AI usage"<sup>[14](#ref14)</sup>.

### OpenAI Verification Problems

OpenAI's verification system has experienced significant technical challenges, with users reporting broken verification links and inability to restart verification processes[15]. Multiple users have documented issues where verification fails repeatedly with messages stating "unable to verify your identity," creating barriers for legitimate enterprise customers seeking to access advanced models<sup>[15](#ref15)</sup>. These technical failures highlight the complexity of implementing robust verification systems at scale<sup>[15](#ref15)</sup>.

### Marketplace Trust Gaps

Current AI marketplaces suffer from several trust-related issues:

**Identity Verification Challenges**: Research indicates that "most organizations don't have a strategy for managing" AI agents, despite expected explosive growth<sup>[1](#ref1)</sup>. The lack of proper identity verification systems means that enterprises cannot reliably determine the authenticity and provenance of AI agents<sup>[16](#ref16)</sup>.

**Fake Agent Proliferation**: Similar to concerns in other digital marketplaces, AI platforms face risks from "fake sellers" and compromised agents<sup>[17](#ref17)</sup>. The ease of creating convincing AI agents makes it difficult for enterprises to distinguish between legitimate and potentially malicious offerings<sup>[9](#ref9)</sup>.

**Lack of Transparency**: AI agents operate without sufficient transparency regarding their training data, algorithms, and decision-making processes<sup>[11](#ref11)</sup>. This opacity creates significant trust barriers for enterprises that need to understand and validate the systems they deploy<sup>[16](#ref16)</sup>.

## IP Protection Concerns Limiting AI Agent Adoption

### Proprietary Algorithm Exposure

Enterprises face significant intellectual property risks when using AI agents, particularly regarding training data and model architecture exposure<sup>[18](#ref18)</sup>. The intersection between AI and intellectual property has led to "a whole range of new and complex IP challenges," with multiple ongoing legal cases against organizations that have released AI generation tools<sup>[18](#ref18)</sup>.

### Financial Services IP Concerns

In the financial sector, substantial barriers including "proprietary data and specialized knowledge, persist between the finance sector and the AI community"<sup>[19](#ref19)</sup>. These barriers impede effective collaboration and limit the ability to deploy AI agents that require access to sensitive financial algorithms and trading strategies<sup>[19](#ref19)</sup>.

### Healthcare Data Sensitivity

Healthcare organizations face particular challenges with AI agent deployment due to stringent data privacy requirements and intellectual property concerns<sup>[20](#ref20)</sup>. The need to protect patient data while enabling AI functionality creates complex verification requirements that current systems struggle to address<sup>[21](#ref21)</sup>.

### Enterprise Reluctance to Share Algorithms

Many enterprises avoid AI agent deployment due to concerns about revealing proprietary algorithms or competitive advantages<sup>[22](#ref22)</sup>. This reluctance is particularly pronounced in manufacturing and technology sectors where algorithmic innovations represent core business value<sup>[23](#ref23)</sup>.

## Financial Losses and Risks from Unverified AI Agents

### Direct Financial Impact Cases

**Air Canada Chatbot Liability**: One of the most prominent cases involved Air Canada's chatbot providing incorrect information about bereavement fares, resulting in the airline being ordered to pay $812.02 in damages<sup>[24](#ref24)</sup><sup>[25](#ref25)</sup>. The case established that companies remain liable for misinformation provided by their AI agents, with the tribunal stating that "it should be obvious to Air Canada that it is responsible for all the information on its website"<sup>[25](#ref25)</sup>.

**Banking Sector Risks**: AI hallucinations pose "substantial risks to banking services" with potentially wide-ranging impacts<sup>[26](#ref26)</sup>. When banking chatbots or financial advisors provide incorrect information about account terms or investment strategies, the consequences can affect both institutions and their customers<sup>[26](#ref26)</sup>.

### Operational and Compliance Risks

**Legal Consequences**: The legal profession has experienced significant AI-related failures, including a 2023 case where attorneys submitted a legal brief citing six non-existent court cases generated by ChatGPT<sup>[26](#ref26)</sup>. Such incidents highlight the compliance risks enterprises face when deploying unverified AI agents<sup>[26](#ref26)</sup>.

**Discrimination Lawsuits**: The Mobley v. Workday lawsuit alleges that automated resume screening tools discriminate based on race, age, and disability status<sup>[27](#ref27)</sup>. The plaintiff applied for over 80 jobs using Workday's screening tool and was rejected every time, highlighting the financial and reputational risks of biased AI systems<sup>[27](#ref27)</sup><sup>[28](#ref28)</sup>.

### Breach and Security Costs

Recent data shows that 74% of organizations report definitely knowing they had an AI breach in 2024, up from 67% in the previous year<sup>[29](#ref29)</sup>. Nearly half (45%) of organizations opted not to report AI-related security breaches due to concerns over reputational damage<sup>[29](#ref29)</sup>. The material impact is significant, with 89% of organizations stating that most or all AI models in production are critical to their success<sup>[29](#ref29)</sup>.

## Industry Reports on AI Agent Adoption Barriers

### 2024 Enterprise Survey Findings

According to comprehensive industry research, significant barriers continue to impede AI agent adoption:

**Security Concerns Dominate**: A survey of over 1,000 enterprise technology leaders revealed that both leadership (53%) and practitioners (62%) identified security concerns as the top challenge in developing and deploying AI agents[5]. These security issues represent the most significant barrier to enterprise adoption<sup>[5](#ref5)</sup>.

**Integration Complexity**: The research found that 42% of enterprises require access to eight or more data sources to deploy AI agents successfully<sup>[5](#ref5)</sup>. Additionally, more than 86% of enterprises require upgrades to their existing technology stack to deploy AI agents<sup>[5](#ref5)</sup>.

**Investment vs. Readiness Gap**: While 42% of enterprises plan to build over 100 AI agent prototypes and 68% budget $500,000 or more annually on AI agent initiatives, nearly half (48%) report their existing integration platforms are only "somewhat ready" for AI's data demands<sup>[5](#ref5)</sup>.

### Skills and Expertise Barriers

Industry data reveals critical capability gaps:

**Talent Shortage**: 35% of organizations cite lack of skills and expertise as a top barrier to adopting AI, including agentic AI<sup>[30](#ref30)</sup>. This skills gap is particularly pronounced in specialized areas like AI agent development and management<sup>[30](#ref30)</sup>.

**Technical Integration Challenges**: 35% of organizations identify tech integration and migration challenges as a primary barrier to AI adoption<sup>[30](#ref30)</sup>. The complexity of integrating AI agents with existing enterprise systems creates significant implementation hurdles<sup>[30](#ref30)</sup>.

### Trust and Governance Issues

**Governance Uncertainty**: 76% of organizations report ongoing internal debate about which teams should control AI security<sup>[29](#ref29)</sup>. This lack of clear governance structures impedes effective AI agent deployment and management<sup>[29](#ref29)</sup>.

**Compliance Concerns**: Nearly 45% of organizations cited data accuracy or bias concerns as a top obstacle to AI adoption<sup>[4](#ref4)</sup>. These concerns are particularly acute for AI agents that make autonomous decisions without human oversight<sup>[4](#ref4)</sup>.

### Market Reality vs. Expectations

**Production Challenges**: Recent BCG research shows that only 25% of AI pilots made it to production<sup>[4](#ref4)</sup>. The 70-20-10 principle reveals that approximately 70% of AI implementation challenges stem from people- and process-related issues, 20% from technology problems, and only 10% from AI algorithms<sup>[2](#ref2)</sup>.

**ROI Uncertainty**: Cost and ROI uncertainty represent significant barriers, with many organizations struggling to demonstrate clear value from AI agent investments<sup>[31](#ref31)</sup>. The average organization scraps 46% of AI proof-of-concepts before they reach production<sup>[31](#ref31)</sup>.

## Implications for Zero-Knowledge Proof Solutions

The comprehensive analysis of AI agent verification challenges reveals a clear market need for innovative solutions like zero-knowledge proof systems. Current verification methods are inadequate for the complex, dynamic nature of AI agents, while trust issues in existing marketplaces and significant IP protection concerns create substantial barriers to adoption.

The financial risks associated with unverified AI agents, from direct liability cases like Air Canada to broader security breaches affecting 74% of organizations, underscore the urgent need for better verification mechanisms. With the AI agents market projected to grow at 46.3% CAGR and potentially contribute $19.9 trillion to the global economy, addressing these verification and trust challenges represents both a significant opportunity and necessity.

Zero-knowledge proof systems could address many of these challenges by enabling AI agents to prove their capabilities without revealing proprietary algorithms, providing the transparency enterprises need while protecting intellectual property. This approach could help bridge the current gap between AI agent potential and enterprise adoption, facilitating the secure and trustworthy deployment of AI agents at scale.

<a name="ref1"></a>[1] https://www.biometricupdate.com/202505/ai-agents-are-a-digital-identity-headache-despite-explosive-growth
<a name="ref2"></a>[2] https://www.bcg.com/press/24october2024-ai-adoption-in-2024-74-of-companies-struggle-to-achieve-and-scale-value
<a name="ref3"></a>[3] https://www.helpnetsecurity.com/2025/05/30/ai-agents-organizations-risk/
<a name="ref4"></a>[4] https://www.linkedin.com/pulse/choke-points-enterprise-ai-adoption-ashish-bhatia-txsve
<a name="ref5"></a>[5] https://www.architectureandgovernance.com/artificial-intelligence/new-research-uncovers-top-challenges-in-enterprise-ai-agent-adoption/
<a name="ref6"></a>[6] https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai
<a name="ref7"></a>[7] https://link.springer.com/10.1007/s10278-024-01147-1
<a name="ref8"></a>[8] https://www.bankofengland.co.uk/financial-stability-in-focus/2025/april-2025
<a name="ref9"></a>[9] https://madison-technologies.com/challenges-of-agentic-ai-can-businesses-trust-autonomous-ai/
<a name="ref10"></a>[10] https://www.semanticscholar.org/paper/1a536b4f5bafbf6f46d474bdc971fc83c5e93544
<a name="ref11"></a>[11] https://huggingface.co/blog/ethics-soc-7
<a name="ref12"></a>[12] https://arxiv.org/abs/2409.11411
<a name="ref13"></a>[13] https://arxiv.org/abs/2412.07822
<a name="ref14"></a>[14] https://www.pointguardai.com/blog/hugging-face-has-become-a-malware-magnet
<a name="ref15"></a>[15] https://community.openai.com/t/verification-issue-on-second-attempt/1231256
<a name="ref16"></a>[16] https://www.identity.com/why-ai-agents-need-verified-digital-identities/
<a name="ref17"></a>[17] https://ieeexplore.ieee.org/document/10401714/
<a name="ref18"></a>[18] https://www.deloitte.com/uk/en/Industries/technology/blogs/intellectual-property-and-generative-ai.html
<a name="ref19"></a>[19] https://arxiv.org/abs/2405.14767
<a name="ref20"></a>[20] https://www.mdpi.com/2076-3417/14/23/10899
<a name="ref21"></a>[21] https://global-us.mellbaou.com/index.php/global/article/view/237
<a name="ref22"></a>[22] https://arxiv.org/abs/2407.20447
<a name="ref23"></a>[23] https://sciresjournals.com/ijstra/node/589
<a name="ref24"></a>[24] https://www.forbes.com/sites/marisagarcia/2024/02/19/what-air-canada-lost-in-remarkable-lying-ai-chatbot-case/
<a name="ref25"></a>[25] https://www.mccarthy.ca/en/insights/blogs/techlex/moffatt-v-air-canada-misrepresentation-ai-chatbot
<a name="ref26"></a>[26] https://www.ayadata.ai/everything-you-need-to-know-about-ai-hallucinations/
<a name="ref27"></a>[27] https://fairnow.ai/workday-lawsuit-resume-screening/
<a name="ref28"></a>[28] https://setyanlaw.com/discriminated-against-by-artificial-intelligence-ai-algorithmic-bias/
<a name="ref29"></a>[29] https://hiddenlayer.com/innovation-hub/hiddenlayer-ai-threat-landscape-report-reveals-ai-breaches-on-the-rise/
<a name="ref30"></a>[30] https://www.pragmaticcoders.com/resources/ai-agent-statistics
<a name="ref31"></a>[31] https://www.ciodive.com/news/AI-project-fail-data-SPGlobal/742590/
<a name="ref32"></a>[32] https://www.semanticscholar.org/paper/1fe69e3fea28bc4468d8947c6df66ba37ba332ec
<a name="ref33"></a>[33] https://francis-press.com/papers/16906
<a name="ref34"></a>[34] https://ieeexplore.ieee.org/document/10645547/
<a name="ref35"></a>[35] https://ieeexplore.ieee.org/document/10773821/
<a name="ref36"></a>[36] https://finance.yahoo.com/news/artificial-intelligence-market-size-worth-154100049.html
<a name="ref37"></a>[37] https://www.ibm.com/think/insights/ai-agent-governance
<a name="ref38"></a>[38] https://www.langchain.com/stateofaiagents
<a name="ref39"></a>[39] https://www.rapidinnovation.io/post/ai-agents-for-kyc-verification
<a name="ref40"></a>[40] https://www.biometricupdate.com/202411/ai-agents-privacy-and-authentication-examined-in-new-report
<a name="ref41"></a>[41] https://www.salesforce.com/blog/unified-trust-security-governance-for-agentic-solutions/
<a name="ref42"></a>[42] https://www.youtube.com/watch?v=vn3eIvrxlUc
<a name="ref43"></a>[43] https://arxiv.org/abs/2408.05354
<a name="ref44"></a>[44] https://www.tandfonline.com/doi/full/10.1080/1553118X.2025.2462087
<a name="ref45"></a>[45] https://ieeexplore.ieee.org/document/10697454/
<a name="ref46"></a>[46] https://ieeexplore.ieee.org/document/9766399/
<a name="ref47"></a>[47] https://ieeexplore.ieee.org/document/10466733/
<a name="ref48"></a>[48] https://openaccess.cms-conferences.org/publications/book/978-1-964867-14-4/article/978-1-964867-14-4_11
<a name="ref49"></a>[49] https://huggingface.co/papers/2502.02649
<a name="ref50"></a>[50] https://www.reddit.com/r/LocalLLaMA/comments/1im7un9/hugging_face_ai_agents_course_is_live/
<a name="ref51"></a>[51] https://huggingface.co/blog/Kseniase/a2a
<a name="ref52"></a>[52] https://www.biometricupdate.com/202406/authenticid-develops-proprietary-algorithms-to-mitigate-biometric-injection-attacks
<a name="ref53"></a>[53] https://www.reddit.com/r/OpenAI/comments/145rolz/openai_suddenly_wants_me_to_verify_my_identity/
<a name="ref54"></a>[54] https://wjarr.com/node/14868
<a name="ref55"></a>[55] https://www.nature.com/articles/s41598-024-79177-6
<a name="ref56"></a>[56] https://www.mdpi.com/2673-2688/5/4/123
<a name="ref57"></a>[57] http://medrxiv.org/lookup/doi/10.1101/2024.12.16.24318586
<a name="ref58"></a>[58] https://www.forumvc.com/2024-the-rise-of-agentic-ai-in-the-enterprise
<a name="ref59"></a>[59] https://www.galaksiya.com/articles/the-ai-agent-revolution-4-barriers-enterprises-must-overcome
<a name="ref60"></a>[60] https://guptadeepak.com/the-future-of-ai-agent-authentication-ensuring-security-and-privacy-in-autonomous-systems/
<a name="ref61"></a>[61] https://www.lumenova.ai/blog/ai-agents-potential-risks/
<a name="ref62"></a>[62] https://journalwjaets.com/node/1090
<a name="ref63"></a>[63] https://jisis.org/wp-content/uploads/2024/10/2024.I4.002.pdf
<a name="ref64"></a>[64] https://dl.acm.org/doi/10.1145/3711129.3711261
<a name="ref65"></a>[65] https://ieeexplore.ieee.org/document/11024927/
<a name="ref66"></a>[66] https://arxiv.org/abs/2412.17149
<a name="ref67"></a>[67] https://www.semanticscholar.org/paper/d1cb95374abc156f08c609a950f1c07f1a568cdf
<a name="ref68"></a>[68] https://eajournals.org/ejcsit/vol13-issue20-2025/designing-enterprise-systems-for-the-future-of-financial-services-the-intersection-of-ai-cloud-native-microservices-and-intelligent-data-processing/
<a name="ref69"></a>[69] https://al-kindipublisher.com/index.php/jcsts/article/view/9465
<a name="ref70"></a>[70] https://generativeaienterprise.ai/p/20-must-read-ai-agents-case-studies-bb2cf6f29ed87b92
<a name="ref71"></a>[71] https://www.creolestudios.com/real-world-ai-agent-case-studies/
<a name="ref72"></a>[72] https://www.multimodal.dev/post/useful-ai-agent-case-studies
<a name="ref73"></a>[73] https://www.searchunify.com/blog/ai-agents-useful-case-studies-from-around-the-world/
<a name="ref74"></a>[74] https://www.trustpath.ai/blog/spotting-red-flags-how-to-evaluate-ai-vendors-and-avoid-costly-mistakes
<a name="ref75"></a>[75] https://cointelegraph.com/news/how-zero-knowledge-proofs-can-make-ai-fairer
<a name="ref76"></a>[76] https://www.alvarezandmarsal.com/insights/artificial-intelligence-and-machine-learning-model-forensics
<a name="ref77"></a>[77] https://academic.oup.com/bjrai/article/doi/10.1093/bjrai/ubae009/7687959
<a name="ref78"></a>[78] https://www.tandfonline.com/doi/full/10.1080/1553118X.2024.2436542
<a name="ref79"></a>[79] https://journal.aimintlllc.com/index.php/ITEJ/article/view/12
<a name="ref80"></a>[80] https://ijccd.umsida.ac.id/index.php/ijccd/article/view/1179
<a name="ref81"></a>[81] https://seejph.com/index.php/seejph/article/view/2254
<a name="ref82"></a>[82] https://www.informingscience.org/Publications/5260
<a name="ref83"></a>[83] https://www.statista.com/statistics/1605541/barriers-to-developing-genai-worldwide/
<a name="ref84"></a>[84] https://menlovc.com/2024-the-state-of-generative-ai-in-the-enterprise/
<a name="ref85"></a>[85] https://www.prnewswire.com/news-releases/identity-verification-market-to-grow-by-usd-16-92-billion-2024-2028-driven-by-eid-cards-smart-infrastructure-and-ai-redefining-market-landscape---technavio-302331124.html
<a name="ref86"></a>[86] https://www.reuters.com/business/emerging-economies-lead-way-ai-trust-survey-shows-2025-04-28/
<a name="ref87"></a>[87] https://doi.library.ubc.ca/10.14288/1.0078651
<a name="ref88"></a>[88] https://www.bbc.com/travel/article/20240222-air-canada-chatbot-misinformation-what-travellers-should-know
<a name="ref89"></a>[89] https://www.cbc.ca/news/canada/british-columbia/air-canada-chatbot-lawsuit-1.7116416
<a name="ref90"></a>[90] https://www.americanbar.org/groups/business_law/resources/business-law-today/2024-february/bc-tribunal-confirms-companies-remain-liable-information-provided-ai-chatbot/
<a name="ref91"></a>[91] https://arxiv.org/abs/2405.04294
<a name="ref92"></a>[92] https://arxiv.org/abs/2410.07561
<a name="ref93"></a>[93] https://mmidentity.fmk.sk/wp-content/uploads/2025/01/MI_2024_ENG.pdf#page=569
<a name="ref94"></a>[94] https://arxiv.org/abs/2405.08944
<a name="ref95"></a>[95] https://link.springer.com/10.1007/s12369-022-00951-5
<a name="ref96"></a>[96] https://ieeexplore.ieee.org/document/9025575/
<a name="ref97"></a>[97] https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/why-agents-are-the-next-frontier-of-generative-ai
<a name="ref98"></a>[98] https://jsmc.pk/index.php/jsmc/article/view/957
<a name="ref99"></a>[99] https://www2.deloitte.com/us/en/pages/consulting/articles/state-of-generative-ai-in-enterprise.html
<a name="ref100"></a>[100] https://jurnal.uns.ac.id/bestuur/article/view/61326
<a name="ref101"></a>[101] https://journalijsra.com/node/580
<a name="ref102"></a>[102] https://www.ai21.com/blog/ai-agent-use-cases/
<a name="ref103"></a>[103] https://botpress.com/blog/ai-agent-case-study
<a name="ref104"></a>[104] https://onepetro.org/SPEHSE/proceedings/24HSE/24HSE/D021S019R002/555492
<a name="ref105"></a>[105] https://link.springer.com/10.1007/s00146-024-02096-7
<a name="ref106"></a>[106] https://tobaccocontrol.bmj.com/lookup/doi/10.1136/tc.1.1.37
<a name="ref107"></a>[107] https://www.pinsentmasons.com/out-law/news/air-canada-chatbot-case-highlights-ai-liability-risks