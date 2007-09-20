<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format">

	<xsl:import href="../../custom/corporate_defaults.xsl"/>
	<xsl:import href="../../base/report/rml_template.xsl"/>

	<xsl:template match="/">
		<xsl:call-template name="rml"/>
	</xsl:template>
	<xsl:template name="stylesheet">
		<paraStyle name="login-title" fontName="Helvetica" fontSize="12"/>
		<paraStyle name="login" fontName="Helvetica-Bold" fontSize="16"/>
		<paraStyle name="style1" fontName="Helvetica" fontSize="12" alignment="RIGHT"/>
		<paraStyle name="cost-name" fontName="Helvetica-BoldOblique" fontSize="10" alignment="RIGHT"/>
		<blockTableStyle id="objects">
			 <blockFont name="Helvetica-BoldOblique" size="12" start="0,0" stop="-1,0"/>
			 <blockValign value="TOP"/>
			 <blockAlignment value="RIGHT" start="0,1" stop="1,-1"/>
			 <lineStyle kind="LINEBELOW" start="0,0" stop="-1,0"/>
		</blockTableStyle>
		<blockTableStyle id="object-totals">
			 <blockValign value="TOP"/>
			 <blockAlignment value="RIGHT" start="0,1" stop="1,-1"/>
			 <lineStyle kind="LINEABOVE" start="-1,0" stop="-1,0"/>
			 <lineStyle kind="LINEABOVE" start="-1,-1" stop="-1,-1"/>
		</blockTableStyle>

		<fo:root font-family="Times" font-size="10pt">
			<fo:layout-master-set>
				<fo:simple-page-master master-name="barcodes-page">
						<fo:region-body margin="0.5in" border="0.25pt solid silver" padding="10pt"/>
				</fo:simple-page-master>
		   </fo:layout-master-set>

		<fo:page-sequence master-reference="barcodes-page">

		<fo:flow flow-name="xsl-region-body">
	<xsl:apply-templates/>
</fo:flow>
</fo:page-sequence>
</fo:root>
</xsl:template>
	<xsl:template name="story">
		<xsl:apply-templates select="borderform-list"/>
	</xsl:template>
	<xsl:template match="borderform-list">
		<xsl:apply-templates select="borderform">
			<xsl:sort order="ascending" select="client_info/name"/>
		</xsl:apply-templates>
	</xsl:template>
	<xsl:template match="client_info">
		<para style="style1">
			<b>
				<xsl:value-of select="title"/>
				<xsl:text> </xsl:text>
				<xsl:value-of select="name"/>
			</b>
		</para>
		<para style="style1"><xsl:value-of select="street"/></para>
		<para style="style1"><xsl:value-of select="street2"/></para>
		<para style="style1">
			<xsl:value-of select="zip"/>
			<xsl:text> </xsl:text>
			<xsl:value-of select="city"/>
		</para>
		<para style="style1"><xsl:value-of select="country"/></para>
	</xsl:template>

	<xsl:template match="borderform">
	<setNextTemplate name="other_pages"/>
		<nextFrame/>
		<xsl:apply-templates select="client_info"/>

<!--		<setNextTemplate name="other_pages"/>-->
<!--		<nextFrame/>-->

		<para style="login-title" t="1">Plate Number:</para>
		<para style="login"><xsl:value-of select="login"/></para>

		<spacer length="1cm"/>

		<para>
			<b t="1">Document</b>: <xsl:text t="1">Buyer form</xsl:text>
		</para><para>
			<b t="1">Auction</b>: <xsl:value-of select="title"/>
		</para>
		<xsl:if test="client_info">
			<para>
				<b t="1">Customer Contact</b>:
				<xsl:value-of select="client_info/phone"/>
				<xsl:if test="number(string-length(client_info/mobile) &gt; 0) + number(string-length(client_info/phone) &gt; 0) = 2">
					<xsl:text> - </xsl:text>
				</xsl:if>
				<xsl:value-of select="client_info/mobile"/>
			</para><para>
				<b t="1">Customer Reference</b>: <xsl:value-of select="client_info/ref"/>
			</para>
		</xsl:if>
		<spacer length="1cm"/>
		<xsl:apply-templates select="objects"/>
<!--		<setNextTemplate name="first_page"/>-->
<!--<pageBreak/>-->
	</xsl:template>
	<xsl:template match="objects">
		<blockTable colWidths="1.4cm,1.8cm,9.8cm,1.5cm,2.5cm,2cm,2cm" style="objects">
			<tr>
				<td t="1">Lot</td>
				<td t="1">Cat. N.</td>
				<td t="1">Description</td>
				<td t="1">Paid</td>
				<td t="1">Adj.(EUR)</td>
				<td t="1">Costs</td>
				<td t="1">Total</td>
			</tr>
			<xsl:apply-templates select="object"/>
		</blockTable>
		<condPageBreak height="3.2cm"/>
		<blockTable colWidths="1.4cm,1.8cm,9.8cm,1.5cm,2.5cm,2cm,2cm" style="object-totals">
			<tr>
				<td/>
				<td/>
				<td/>
				<td/>
				<td/>
				<td t="1">Subtotal:</td>
				<td><xsl:value-of select="format-number(sum(object[price != '']/price), '#,##0.00')"/></td>
			</tr>
<!--			<xsl:apply-templates select="cost"/>-->
			<tr>
				<td/>
				<td/>
				<td/>
				<td/>
				<td/>
				<td t="1">Cost:</td>
				<td><xsl:value-of select="format-number(sum(object/cost/amount), '#,##0.00')"/></td>
			</tr>
			<tr>
				<td/>
				<td/>
				<td/>
				<td/>
				<td/>
				<td t="1">Total:</td>
				<td><xsl:value-of select="format-number(sum(object[price != '']/price) + sum(object/cost/amount), '#,##0.00')"/></td>
			</tr>
		</blockTable>
	</xsl:template>



	<xsl:template match="object">
		<tr>
			<td><xsl:value-of select="ref"/><barCode code="code128" x="26.9mm" height="68.1mm" quiet="9" fontName="Times-Roman" fontSize="50"  alignment="CENTER"></barCode></td>
			<td><xsl:value-of select="ref"/></td>
			<td>
				<para>
					<b><xsl:value-of select="title"/><xsl:text>. </xsl:text></b>
					<xsl:value-of select="desc"/>
				</para>
			</td>
			<td><xsl:if test="state='paid'"><xsl:text>X</xsl:text></xsl:if></td>
			<td>
				<xsl:if test="price!=''">
					<xsl:value-of select="format-number(price, '#,##0.00')"/>
				</xsl:if>
			</td>
			<td><xsl:value-of select="format-number(sum(cost/amount), '#,##0.00')"/></td>
			<td>
				<xsl:if test="price!=''">
					<xsl:value-of select="format-number(price + sum(cost/amount), '#,##0.00')"/>
				</xsl:if>
			</td>
		</tr>
</xsl:template>

</xsl:stylesheet>
